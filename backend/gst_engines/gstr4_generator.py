"""GSTR-4 Generator - Return for Composition Taxpayers"""
from typing import List, Dict, Any, Optional
from gst_engines.base_generator import BaseGenerator

class GSTR4Generator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-4")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        total_turnover = sum(r.get('total_value', 0) for r in data)
        taxable_turnover = sum(r.get('taxable_value', 0) for r in data)
        composition_rate = kwargs.get('composition_rate', 0.01)
        tax_payable = taxable_turnover * composition_rate
        
        return {
            'period': period,
            '4_inward_supplies': {'4A_imported_goods': 0, '4B_imported_services': 0,
                                  '4C_inward_supplies_from_registered': 0, '4D_inward_supplies_from_unregistered': 0,
                                  '4E_non_gst_supplies': 0},
            '5_outward_supplies': {'5A_taxable_supplies': round(taxable_turnover, 2), '5B_exempt_supplies': 0,
                                   '5C_exports': 0, '5D_total': round(total_turnover, 2)},
            '6_tax_computation': {'taxable_turnover': round(taxable_turnover, 2), 'composition_rate': composition_rate * 100,
                                  'tax_payable': round(tax_payable, 2), 'interest': 0, 'late_fee': 0,
                                  'total_payable': round(tax_payable, 2)},
            'summary': {'total_turnover': round(total_turnover, 2), 'taxable_turnover': round(taxable_turnover, 2),
                       'tax_payable': round(tax_payable, 2)}
        }
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {
            'period': self.format_period(period),
            '4_inward_supplies': {'4A_imported_goods': 0, '4B_imported_services': 0, '4C_inward_supplies_from_registered': 0,
                                  '4D_inward_supplies_from_unregistered': 0, '4E_non_gst_supplies': 0},
            '5_outward_supplies': {'5A_taxable_supplies': 0, '5B_exempt_supplies': 0, '5C_exports': 0, '5D_total': 0},
            '6_tax_computation': {'taxable_turnover': 0, 'composition_rate': 1, 'tax_payable': 0, 'interest': 0,
                                  'late_fee': 0, 'total_payable': 0},
            'summary': {'total_turnover': 0, 'taxable_turnover': 0, 'tax_payable': 0}
        }
