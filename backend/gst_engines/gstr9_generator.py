"""GSTR-9 Generator - Annual Return"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from gst_engines.base_generator import BaseGenerator

logger = logging.getLogger(__name__)

class GSTR9Generator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-9")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        financial_year = kwargs.get('financial_year', self._get_financial_year())
        outward_supplies = self._calculate_outward_supplies(data)
        itc_details = self._calculate_itc(data)
        tax_paid = self._calculate_tax_paid(data)
        transactions = self._calculate_transactions(data)
        
        return {
            'financial_year': financial_year,
            'part_ii_outward_supplies': outward_supplies,
            'part_iii_itc_details': itc_details,
            'part_iv_tax_paid': tax_paid,
            'part_v_transactions': transactions,
            'summary': {
                'total_outward_value': outward_supplies['total_value'],
                'total_taxable_value': outward_supplies['total_taxable_value'],
                'total_tax_paid': tax_paid['total_tax_paid']
            }
        }
    
    def _calculate_outward_supplies(self, data: List[Dict]) -> Dict:
        taxable = [r for r in data if r.get('tax_rate', 0) > 0]
        taxable_value = sum(r.get('taxable_value', 0) for r in taxable)
        zero_rated = [r for r in data if r.get('tax_rate', 0) == 0]
        zero_rated_value = sum(r.get('taxable_value', 0) for r in zero_rated)
        b2b_value = sum(r.get('taxable_value', 0) for r in data if r.get('supply_type') == 'B2B')
        b2c_value = sum(r.get('taxable_value', 0) for r in data if r.get('supply_type') in ['B2CS', 'B2CL'])
        
        return {
            '4_taxable_supplies': {'b2b_supplies': round(b2b_value, 2), 'b2c_supplies': round(b2c_value, 2), 'total': round(taxable_value, 2)},
            '5_zero_rated_supplies': {'export': 0, 'supplies_to_sez': 0, 'total': round(zero_rated_value, 2)},
            '6_deemed_exports': 0, '7_exempted_supplies': 0, '8_non_gst_supplies': 0,
            '9_reversal_of_credit_notes': 0, '10_addition_debit_notes': 0,
            'total_value': round(sum(r.get('total_value', 0) for r in data), 2),
            'total_taxable_value': round(taxable_value, 2)
        }
    
    def _calculate_itc(self, data: List[Dict]) -> Dict:
        return {
            '12_itc_availed': {'inputs': 0, 'capital_goods': 0, 'input_services': 0, 'total': 0},
            '13_itc_reversed': {'as_per_rules': 0, 'others': 0, 'total': 0},
            '14_net_itc': 0,
            '15_ineligible_itc': {'section_17_5': 0, 'others': 0, 'total': 0}
        }
    
    def _calculate_tax_paid(self, data: List[Dict]) -> Dict:
        igst = sum(r.get('igst', 0) for r in data)
        cgst = sum(r.get('cgst', 0) for r in data)
        sgst = sum(r.get('sgst', 0) for r in data)
        
        return {
            '16_tax_paid_through_itc': {'igst': 0, 'cgst': 0, 'sgst': 0, 'cess': 0, 'total': 0},
            '17_tax_paid_in_cash': {'igst': round(igst, 2), 'cgst': round(cgst, 2), 'sgst': round(sgst, 2), 'cess': 0, 'total': round(igst + cgst + sgst, 2)},
            '18_interest_late_fee': {'interest': 0, 'late_fee': 0, 'total': 0},
            'total_tax_paid': round(igst + cgst + sgst, 2)
        }
    
    def _calculate_transactions(self, data: List[Dict]) -> Dict:
        rate_5 = [r for r in data if 0.04 <= r.get('tax_rate', 0) <= 0.06]
        rate_12 = [r for r in data if 0.11 <= r.get('tax_rate', 0) <= 0.13]
        rate_18 = [r for r in data if 0.17 <= r.get('tax_rate', 0) <= 0.19]
        rate_28 = [r for r in data if 0.27 <= r.get('tax_rate', 0) <= 0.29]
        
        return {
            '19_supplies_at_5_percent': self._rate_summary(rate_5),
            '20_supplies_at_12_percent': self._rate_summary(rate_12),
            '21_supplies_at_18_percent': self._rate_summary(rate_18),
            '22_supplies_at_28_percent': self._rate_summary(rate_28)
        }
    
    def _rate_summary(self, data: List[Dict]) -> Dict:
        return {
            'taxable_value': round(sum(r.get('taxable_value', 0) for r in data), 2),
            'igst': round(sum(r.get('igst', 0) for r in data), 2),
            'cgst': round(sum(r.get('cgst', 0) for r in data), 2),
            'sgst': round(sum(r.get('sgst', 0) for r in data), 2)
        }
    
    def _get_financial_year(self) -> str:
        now = datetime.now()
        if now.month >= 4:
            return f"{now.year}-{now.year + 1}"
        return f"{now.year - 1}-{now.year}"
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {
            'financial_year': self._get_financial_year(),
            'part_ii_outward_supplies': {
                '4_taxable_supplies': {'b2b_supplies': 0, 'b2c_supplies': 0, 'total': 0},
                '5_zero_rated_supplies': {'export': 0, 'supplies_to_sez': 0, 'total': 0},
                '6_deemed_exports': 0, '7_exempted_supplies': 0, '8_non_gst_supplies': 0,
                '9_reversal_of_credit_notes': 0, '10_addition_debit_notes': 0,
                'total_value': 0, 'total_taxable_value': 0
            },
            'part_iii_itc_details': {
                '12_itc_availed': {'inputs': 0, 'capital_goods': 0, 'input_services': 0, 'total': 0},
                '13_itc_reversed': {'as_per_rules': 0, 'others': 0, 'total': 0},
                '14_net_itc': 0,
                '15_ineligible_itc': {'section_17_5': 0, 'others': 0, 'total': 0}
            },
            'part_iv_tax_paid': {
                '16_tax_paid_through_itc': {'igst': 0, 'cgst': 0, 'sgst': 0, 'cess': 0, 'total': 0},
                '17_tax_paid_in_cash': {'igst': 0, 'cgst': 0, 'sgst': 0, 'cess': 0, 'total': 0},
                '18_interest_late_fee': {'interest': 0, 'late_fee': 0, 'total': 0},
                'total_tax_paid': 0
            },
            'part_v_transactions': {
                '19_supplies_at_5_percent': {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0},
                '20_supplies_at_12_percent': {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0},
                '21_supplies_at_18_percent': {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0},
                '22_supplies_at_28_percent': {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0}
            },
            'summary': {'total_outward_value': 0, 'total_taxable_value': 0, 'total_tax_paid': 0}
        }
