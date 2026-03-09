"""GSTR-1 Generator - Monthly/Quarterly return for outward supplies"""
import logging
from typing import List, Dict, Any, Optional
from collections import defaultdict
from gst_engines.base_generator import BaseGenerator

logger = logging.getLogger(__name__)

class GSTR1Generator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-1")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        b2b_data = [r for r in data if r.get('supply_type') == 'B2B']
        b2cl_data = [r for r in data if r.get('supply_type') == 'B2CL']
        b2cs_data = [r for r in data if r.get('supply_type') == 'B2CS']
        
        b2b = self._generate_b2b(b2b_data)
        b2cl = self._generate_b2cl(b2cl_data)
        b2cs = self._generate_b2cs(b2cs_data)
        hsn = self._generate_hsn(data)
        totals = self._calculate_totals(data)
        
        return {
            'period': period,
            'sections': {'b2b': b2b, 'b2cl': b2cl, 'b2cs': b2cs, 'hsn': hsn},
            'totals': totals,
            'summary': {'total_invoices': len(data), 'b2b_invoices': len(b2b_data), 
                       'b2cl_invoices': len(b2cl_data), 'b2cs_invoices': len(b2cs_data)}
        }
    
    def _generate_b2b(self, data: List[Dict]) -> List[Dict]:
        grouped = defaultdict(list)
        for record in data:
            gstin = record.get('customer_gstin', '')
            if gstin:
                grouped[gstin].append(record)
        
        b2b_rows = []
        for gstin, records in grouped.items():
            for record in records:
                b2b_rows.append({
                    'gstin_of_recipient': gstin,
                    'receiver_name': record.get('customer_name', ''),
                    'invoice_number': record.get('invoice_number', ''),
                    'invoice_date': record.get('invoice_date', ''),
                    'invoice_value': round(record.get('total_value', 0), 2),
                    'place_of_supply': record.get('state_code', ''),
                    'reverse_charge': 'N',
                    'invoice_type': 'Regular',
                    'rate': record.get('tax_rate', 0) * 100,
                    'taxable_value': round(record.get('taxable_value', 0), 2),
                    'cgst': round(record.get('cgst', 0), 2),
                    'sgst': round(record.get('sgst', 0), 2),
                    'igst': round(record.get('igst', 0), 2)
                })
        return b2b_rows
    
    def _generate_b2cl(self, data: List[Dict]) -> List[Dict]:
        return [{
            'invoice_number': r.get('invoice_number', ''),
            'invoice_date': r.get('invoice_date', ''),
            'invoice_value': round(r.get('total_value', 0), 2),
            'place_of_supply': r.get('state_code', ''),
            'rate': r.get('tax_rate', 0) * 100,
            'taxable_value': round(r.get('taxable_value', 0), 2),
            'cgst': round(r.get('cgst', 0), 2),
            'sgst': round(r.get('sgst', 0), 2),
            'igst': round(r.get('igst', 0), 2)
        } for r in data]
    
    def _generate_b2cs(self, data: List[Dict]) -> List[Dict]:
        grouped = defaultdict(lambda: {'taxable_value': 0, 'cgst': 0, 'sgst': 0, 'igst': 0})
        for record in data:
            key = (record.get('state_code', ''), record.get('tax_rate', 0))
            grouped[key]['taxable_value'] += record.get('taxable_value', 0)
            grouped[key]['cgst'] += record.get('cgst', 0)
            grouped[key]['sgst'] += record.get('sgst', 0)
            grouped[key]['igst'] += record.get('igst', 0)
        
        return [{'type': 'OE', 'place_of_supply': state_code, 'rate': rate * 100,
                 'taxable_value': round(vals['taxable_value'], 2), 'cgst': round(vals['cgst'], 2),
                 'sgst': round(vals['sgst'], 2), 'igst': round(vals['igst'], 2)}
                for (state_code, rate), vals in grouped.items()]
    
    def _generate_hsn(self, data: List[Dict]) -> List[Dict]:
        return self.aggregate_by_hsn(data)
    
    def _calculate_totals(self, data: List[Dict]) -> Dict:
        return {
            'total_taxable_value': round(sum(r.get('taxable_value', 0) for r in data), 2),
            'total_cgst': round(sum(r.get('cgst', 0) for r in data), 2),
            'total_sgst': round(sum(r.get('sgst', 0) for r in data), 2),
            'total_igst': round(sum(r.get('igst', 0) for r in data), 2),
            'total_value': round(sum(r.get('total_value', 0) for r in data), 2)
        }
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {
            'period': self.format_period(period),
            'sections': {'b2b': [], 'b2cl': [], 'b2cs': [], 'hsn': []},
            'totals': {'total_taxable_value': 0, 'total_cgst': 0, 'total_sgst': 0, 'total_igst': 0, 'total_value': 0},
            'summary': {'total_invoices': 0, 'b2b_invoices': 0, 'b2cl_invoices': 0, 'b2cs_invoices': 0}
        }
