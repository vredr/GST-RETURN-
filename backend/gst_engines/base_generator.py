"""Base Generator for all GST returns"""
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseGenerator(ABC):
    def __init__(self, return_type: str):
        self.return_type = return_type
    
    @abstractmethod
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        pass
    
    def validate_data(self, data: List[Dict]) -> bool:
        if not data:
            logger.warning("No data provided for return generation")
            return False
        return True
    
    def format_period(self, period: Optional[str]) -> str:
        if not period:
            now = datetime.now()
            return f"{now.month:02d}-{now.year}"
        return period
    
    def aggregate_by_hsn(self, data: List[Dict]) -> List[Dict]:
        hsn_summary = {}
        for record in data:
            hsn = record.get('hsn_code', 'NA')
            tax_rate = record.get('tax_rate', 0)
            key = f"{hsn}_{tax_rate}"
            if key not in hsn_summary:
                hsn_summary[key] = {'hsn_code': hsn, 'tax_rate': tax_rate, 'total_quantity': 0, 'total_value': 0,
                                    'taxable_value': 0, 'cgst': 0, 'sgst': 0, 'igst': 0}
            hsn_summary[key]['total_quantity'] += record.get('quantity', 0)
            hsn_summary[key]['total_value'] += record.get('total_value', 0)
            hsn_summary[key]['taxable_value'] += record.get('taxable_value', 0)
            hsn_summary[key]['cgst'] += record.get('cgst', 0)
            hsn_summary[key]['sgst'] += record.get('sgst', 0)
            hsn_summary[key]['igst'] += record.get('igst', 0)
        return list(hsn_summary.values())
