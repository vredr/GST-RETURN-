"""
TaxNow - GST Compliance SaaS Platform
Main FastAPI Application - Production Ready
"""

import os
import uuid
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import pandas as pd

from core.config import settings
from core.database import Database
from core.schema_converter import SchemaConverter
from core.gst_return_router import GSTRouter
from marketplace_parsers.parser_factory import ParserFactory
from models.gst_models import (
    UploadResponse, ProcessResponse, GSTSummary, MarketplaceType, ReturnType
)
from utils.file_handler import FileHandler
from utils.excel_generator import ExcelGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = Database()
file_handler = FileHandler()
schema_converter = SchemaConverter()
gst_router = GSTRouter()
excel_generator = ExcelGenerator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting TaxNow GST Platform...")
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(
    title="TaxNow GST API",
    description="GST Compliance Platform for Indian E-commerce Sellers",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TaxNow GST API", "version": "2.0.0", "status": "active", "docs": "/docs"}

@app.get("/health")
async def health_check():
    try:
        db_status = await db.health_check()
        return {"status": "healthy", "database": db_status, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/upload", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    marketplace: str = Form(...),
    file: UploadFile = File(...),
    business_id: Optional[str] = Form(None),
    supplier_state: Optional[str] = Form("Maharashtra")
):
    try:
        valid_marketplaces = [m.value for m in MarketplaceType]
        if marketplace not in valid_marketplaces:
            raise HTTPException(status_code=400, detail=f"Invalid marketplace. Supported: {valid_marketplaces}")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.xlsx', '.xls', '.csv']:
            raise HTTPException(status_code=400, detail="Only Excel or CSV files supported")
        
        content = await file.read()
        if len(content) > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 50MB")
        await file.seek(0)
        
        upload_id = str(uuid.uuid4())
        file_path = await file_handler.save_upload(file, upload_id)
        
        parser = ParserFactory.get_parser(marketplace)
        raw_data = parser.parse(file_path)
        
        if not raw_data:
            raise HTTPException(status_code=400, detail="No data found in file")
        
        await db.store_raw_data(upload_id, marketplace, raw_data, business_id)
        background_tasks.add_task(file_handler.cleanup, file_path)
        
        return UploadResponse(
            upload_id=upload_id,
            filename=file.filename,
            marketplace=marketplace,
            total_records=len(raw_data),
            status="uploaded",
            message="File uploaded successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process", response_model=ProcessResponse)
async def process_data(
    upload_id: str,
    supplier_gstin: Optional[str] = None,
    supplier_state: str = "Maharashtra"
):
    try:
        raw_data = await db.get_raw_data(upload_id)
        if not raw_data:
            raise HTTPException(status_code=404, detail="Upload ID not found")
        
        normalized_data = schema_converter.convert(raw_data['data'], raw_data['marketplace'], supplier_state, supplier_gstin)
        if not normalized_data:
            raise HTTPException(status_code=400, detail="No valid data could be normalized")
        
        classified_data = schema_converter.classify_transactions(normalized_data, supplier_state)
        processed_data = schema_converter.calculate_gst(classified_data, supplier_state)
        
        await db.store_processed_data(upload_id, processed_data)
        summary = schema_converter.generate_summary(processed_data)
        
        return ProcessResponse(
            upload_id=upload_id,
            total_invoices=len(processed_data),
            b2b_count=summary['b2b_count'],
            b2cl_count=summary['b2cl_count'],
            b2cs_count=summary['b2cs_count'],
            total_taxable_value=summary['total_taxable_value'],
            total_cgst=summary['total_cgst'],
            total_sgst=summary['total_sgst'],
            total_igst=summary['total_igst'],
            status="processed",
            message="Data processed successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-return")
async def generate_return(
    upload_id: str,
    return_type: ReturnType = Query(...),
    period: Optional[str] = Query(None),
    download: bool = Query(False)
):
    try:
        processed_data = await db.get_processed_data(upload_id)
        if not processed_data:
            raise HTTPException(status_code=404, detail="Processed data not found")
        
        return_data = gst_router.generate(return_type.value, processed_data['data'], period=period)
        
        if download:
            output_path = excel_generator.create_return_excel(return_type.value, return_data, upload_id)
            return FileResponse(
                output_path,
                filename=f"{return_type.value.upper()}_{period or 'current'}_{upload_id[:8]}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        return {"upload_id": upload_id, "return_type": return_type.value, "period": period, "data": return_data, "status": "generated"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Return generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-report")
async def download_report(upload_id: str, report_type: str = Query("summary")):
    try:
        processed_data = await db.get_processed_data(upload_id)
        if not processed_data:
            raise HTTPException(status_code=404, detail="Data not found")
        
        if report_type == "summary":
            output_path = excel_generator.create_summary_report(processed_data['data'], upload_id)
        elif report_type == "hsn":
            output_path = excel_generator.create_hsn_summary(processed_data['data'], upload_id)
        elif report_type == "tax_summary":
            output_path = excel_generator.create_tax_summary(processed_data['data'], upload_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid report type")
        
        return FileResponse(output_path, filename=f"{report_type}_{upload_id[:8]}.xlsx")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/marketplaces")
async def get_marketplaces():
    return {"marketplaces": [{"id": m.value, "name": m.name.replace("_", " ").title()} for m in MarketplaceType]}

@app.get("/return-types")
async def get_return_types():
    descriptions = {
        "gstr1": "Monthly/Quarterly return for outward supplies",
        "gstr3b": "Monthly summary return",
        "gstr2a": "Auto-drafted details of inward supplies",
        "gstr2b": "Static ITC statement",
        "gstr4": "Return for composition taxpayers",
        "gstr5": "Return for non-resident foreign taxpayers",
        "gstr6": "Return for input service distributors",
        "gstr7": "Return for TDS deductors",
        "gstr8": "Return for e-commerce operators",
        "gstr9": "Annual return",
        "gstr9c": "Reconciliation statement",
        "gstr10": "Final return",
        "gstr11": "Return for UIN holders"
    }
    return {"return_types": [{"id": r.value, "name": r.name.replace("_", "-").replace("GSTR", "GSTR-"), "description": descriptions.get(r.value, "GST Return")} for r in ReturnType]}

@app.get("/gst-summary/{upload_id}")
async def get_gst_summary(upload_id: str):
    try:
        processed_data = await db.get_processed_data(upload_id)
        if not processed_data:
            raise HTTPException(status_code=404, detail="Data not found")
        summary = schema_converter.generate_summary(processed_data['data'])
        return GSTSummary(**summary)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
