"""GSTR-8 Generator - Return for E-commerce Operators"""
from typing import List, Dict, Any, Optional
from collections import defaultdict
from gst_engines.base_generator import BaseGenerator

class GSTR8Generator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-8")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        tcs_rate = 0.01
        tcs_details = self._calculate_tcs(data, tcs_rate)
        
        return {
            'period': period,
            '3_tcs_collected': tcs_details['collections'],
            '4_amendments': [],
            '5_interest_late_fee': {'interest': 0, 'late_fee': 0},
            'summary': {'total_supplies_value': tcs_details['total_value'], 'total_tcs_collected': tcs_details['total_tcs'],
                       'total_igst': tcs_details['total_igst'], 'total_cgst': tcs_details['total_cgst'],
                       'total_sgst': tcs_details['total_sgst']}
        }
    
    def _calculate_tcs(self, data: List[Dict], tcs_rate: float) -> Dict:
        grouped = defaultdict(lambda: {'taxable_value': 0, 'total_value': 0, 'is_interstate': False})
        for record in data:
            gstin = record.get('customer_gstin', '')
            if gstin:
                grouped[gstin]['taxable_value'] += record.get('taxable_value', 0)
                grouped[gstin]['total_value'] += record.get('total_value', 0)
                grouped[gstin]['is_interstate'] = record.get('is_interstate', False)
        
        collections = []
        total_tcs = total_igst = total_cgst = total_sgst = total_value = 0
        
        for gstin, values in grouped.items():
            taxable = values['taxable_value']
            total_val = values['total_value']
            is_interstate = values['is_interstate']
            total_value += total_val
            
            if is_interstate:
                igst = round(taxable * tcs_rate, 2)
                cgst = sgst = 0
                total_igst += igst
            else:
                igst = 0
                cgst = round(taxable * 0.005, 2)
                sgst = round(taxable * 0.005, 2)
                total_cgst += cgst
                total_sgst += sgst
            
            tcs_amount = igst + cgst + sgst
            total_tcs += tcs_amount
            
            collections.append({'gstin_of_supplier': gstin, 'gross_value_of_supplies': round(total_val, 2),
                                'taxable_value': round(taxable, 2), 'tcs_rate': tcs_rate * 100,
                                'igst': igst, 'cgst': cgst, 'sgst': sgst, 'total_tcs': round(tcs_amount, 2)})
        
        return {'collections': collections, 'total_value': round(total_value, 2), 'total_tcs': round(total_tcs, 2),
                'total_igst': round(total_igst, 2), 'total_cgst': round(total_cgst, 2), 'total_sgst': round(total_sgst, 2)}
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {'period': self.format_period(period), '3_tcs_collected': [], '4_amendments': [],
                '5_interest_late_fee': {'interest': 0, 'late_fee': 0},
                'summary': {'total_supplies_value': 0, 'total_tcs_collected': 0, 'total_igst': 0,
                           'total_cgst': 0, 'total_sgst': 0}}
