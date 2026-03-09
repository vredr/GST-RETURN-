"""Excel Generator Utility"""
import logging
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
from core.config import settings

logger = logging.getLogger(__name__)

class ExcelGenerator:
    def __init__(self):
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_return_excel(self, return_type: str, return_data: Dict, upload_id: str) -> str:
        output_path = self.output_dir / f"{return_type}_{upload_id}.xlsx"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if return_type == 'gstr1':
                self._write_gstr1(writer, return_data)
            elif return_type == 'gstr3b':
                self._write_gstr3b(writer, return_data)
            elif return_type == 'gstr9':
                self._write_gstr9(writer, return_data)
            else:
                self._write_generic(writer, return_data)
        
        logger.info(f"Created Excel: {output_path}")
        return str(output_path)
    
    def _write_gstr1(self, writer: pd.ExcelWriter, data: Dict):
        sections = data.get('sections', {})
        for sheet_name, sheet_data in sections.items():
            if sheet_data:
                df = pd.DataFrame(sheet_data)
                df.to_excel(writer, sheet_name=sheet_name.upper(), index=False)
        
        totals = data.get('totals', {})
        summary = data.get('summary', {})
        summary_df = pd.DataFrame([{**totals, **summary}])
        summary_df.to_excel(writer, sheet_name='SUMMARY', index=False)
    
    def _write_gstr3b(self, writer: pd.ExcelWriter, data: Dict):
        outward = data.get('3_1_tax_on_outward_supplies', {})
        outward_rows = [{k: v for k, v in outward.items() if isinstance(v, dict)}]
        if outward_rows:
            pd.DataFrame(outward_rows).to_excel(writer, sheet_name='3.1 Outward', index=False)
        
        hsn_data = data.get('hsn_summary', [])
        if hsn_data:
            pd.DataFrame(hsn_data).to_excel(writer, sheet_name='HSN Summary', index=False)
    
    def _write_gstr9(self, writer: pd.ExcelWriter, data: Dict):
        outward = data.get('part_ii_outward_supplies', {})
        if outward:
            pd.DataFrame([outward]).to_excel(writer, sheet_name='Outward Supplies', index=False)
    
    def _write_generic(self, writer: pd.ExcelWriter, data: Dict):
        for key, value in data.items():
            if isinstance(value, list) and value:
                try:
                    df = pd.DataFrame(value)
                    sheet_name = key[:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                except Exception as e:
                    logger.warning(f"Could not write sheet {key}: {e}")
    
    def create_summary_report(self, data: List[Dict], upload_id: str) -> str:
        output_path = self.output_dir / f"summary_{upload_id}.xlsx"
        df = pd.DataFrame(data)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All Invoices', index=False)
            
            if 'supply_type' in df.columns:
                supply_summary = df.groupby('supply_type').agg({
                    'taxable_value': 'sum', 'cgst': 'sum', 'sgst': 'sum', 'igst': 'sum', 'total_value': 'sum'
                }).reset_index()
                supply_summary.to_excel(writer, sheet_name='By Supply Type', index=False)
        
        return str(output_path)
    
    def create_hsn_summary(self, data: List[Dict], upload_id: str) -> str:
        output_path = self.output_dir / f"hsn_summary_{upload_id}.xlsx"
        df = pd.DataFrame(data)
        
        if 'hsn_code' in df.columns:
            hsn_summary = df.groupby(['hsn_code', 'tax_rate']).agg({
                'quantity': 'sum', 'taxable_value': 'sum', 'cgst': 'sum', 'sgst': 'sum', 'igst': 'sum', 'total_value': 'sum'
            }).reset_index()
        else:
            hsn_summary = df
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            hsn_summary.to_excel(writer, sheet_name='HSN Summary', index=False)
        
        return str(output_path)
    
    def create_tax_summary(self, data: List[Dict], upload_id: str) -> str:
        output_path = self.output_dir / f"tax_summary_{upload_id}.xlsx"
        df = pd.DataFrame(data)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if 'tax_rate' in df.columns:
                rate_summary = df.groupby('tax_rate').agg({
                    'taxable_value': 'sum', 'cgst': 'sum', 'sgst': 'sum', 'igst': 'sum', 'total_value': 'sum'
                }).reset_index()
                rate_summary.to_excel(writer, sheet_name='By Tax Rate', index=False)
        
        return str(output_path)
