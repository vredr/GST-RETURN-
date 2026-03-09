"""GST Data Models"""
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class MarketplaceType(str, Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MEESHO = "meesho"
    SHOPIFY = "shopify"
    WOOCOMMERCE = "woocommerce"
    SNAPDEAL = "snapdeal"
    INDIAMART = "indiamart"
    AJIO = "ajio"
    MYNTRA = "myntra"
    JIOMART = "jiomart"
    GENERIC = "generic"

class ReturnType(str, Enum):
    GSTR1 = "gstr1"
    GSTR3B = "gstr3b"
    GSTR2A = "gstr2a"
    GSTR2B = "gstr2b"
    GSTR4 = "gstr4"
    GSTR5 = "gstr5"
    GSTR6 = "gstr6"
    GSTR7 = "gstr7"
    GSTR8 = "gstr8"
    GSTR9 = "gstr9"
    GSTR9C = "gstr9c"
    GSTR10 = "gstr10"
    GSTR11 = "gstr11"

class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    marketplace: str
    total_records: int
    status: str
    message: str

class ProcessResponse(BaseModel):
    upload_id: str
    total_invoices: int
    b2b_count: int
    b2cl_count: int
    b2cs_count: int
    total_taxable_value: float
    total_cgst: float
    total_sgst: float
    total_igst: float
    status: str
    message: str

class GSTSummary(BaseModel):
    total_invoices: int
    b2b_count: int
    b2cl_count: int
    b2cs_count: int
    total_taxable_value: float
    total_cgst: float
    total_sgst: float
    total_igst: float
    total_tax: float
