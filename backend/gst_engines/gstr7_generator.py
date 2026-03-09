"""GSTR-7 Generator - Return for TDS Deductors"""
from typing import List, Dict, Any, Optional
from collections import defaultdict
from gst_engines.base_generator import BaseGenerator

class GSTR7Generator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-7")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        tds_rate = 0.02
        tds_details = self._calculate_tds(data, tds_rate)
        
        return {
            'period': period,
            '3_tds_deducted': tds_details['deductions'],
            '4_amendments': [],
            '5_interest_late_fee': {'interest': 0, 'late_fee': 0},
            'summary': {'total_tds_deducted': tds_details['total_tds'], 'total_igst': tds_details['total_igst'],
                       'total_cgst': tds_details['total_cgst'], 'total_sgst': tds_details['total_sgst']}
        }
    
    def _calculate_tds(self, data: List[Dict], tds_rate: float) -> Dict:
        grouped = defaultdict(lambda: {'taxable_value': 0, 'is_interstate': False})
        for record in data:
            gstin = record.get('customer_gstin', '')
            if gstin:
                grouped[gstin]['taxable_value'] += record.get('taxable_value', 0)
                grouped[gstin]['is_interstate'] = record.get('is_interstate', False)
        
        deductions = []
        total_tds = total_igst = total_cgst = total_sgst = 0
        
        for gstin, values in grouped.items():
            taxable = values['taxable_value']
            is_interstate = values['is_interstate']
            
            if is_interstate:
                igst = round(taxable * tds_rate, 2)
                cgst = sgst = 0
                total_igst += igst
            else:
                igst = 0
                cgst = round(taxable * 0.01, 2)
                sgst = round(taxable * 0.01, 2)
                total_cgst += cgst
                total_sgst += sgst
            
            tds_amount = igst + cgst + sgst
            total_tds += tds_amount
            
            deductions.append({'gstin_of_deductee': gstin, 'amount_paid': round(taxable, 2),
                               'tds_rate': tds_rate * 100, 'igst': igst, 'cgst': cgst, 'sgst': sgst,
                               'total_tds': round(tds_amount, 2)})
        
        return {'deductions': deductions, 'total_tds': round(total_tds, 2), 'total_igst': round(total_igst, 2),
                'total_cgst': round(total_cgst, 2), 'total_sgst': round(total_sgst, 2)}
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {'period': self.format_period(period), '3_tds_deducted': [], '4_amendments': [],
                '5_interest_late_fee': {'interest': 0, 'late_fee': 0},
                'summary': {'total_tds_deducted': 0, 'total_igst': 0, 'total_cgst': 0, 'total_sgst': 0}}
