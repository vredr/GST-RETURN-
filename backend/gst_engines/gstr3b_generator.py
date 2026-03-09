"""GSTR-3B Generator - Monthly summary return"""
import logging
from typing import List, Dict, Any, Optional
from gst_engines.base_generator import BaseGenerator

logger = logging.getLogger(__name__)

class GSTR3BGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-3B")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        outward_supplies = self._calculate_outward_supplies(data)
        inter_state = self._calculate_inter_state(data)
        hsn_summary = self.aggregate_by_hsn(data)
        
        return {
            'period': period,
            '3_1_tax_on_outward_supplies': outward_supplies,
            '3_2_inter_state_supplies': inter_state,
            'hsn_summary': hsn_summary,
            'total_liability': {
                'taxable_value': outward_supplies['total_taxable_value'],
                'igst': outward_supplies['integrated_tax'],
                'cgst': outward_supplies['central_tax'],
                'sgst': outward_supplies['state_tax'],
                'cess': 0
            }
        }
    
    def _calculate_outward_supplies(self, data: List[Dict]) -> Dict:
        b2b_data = [r for r in data if r.get('supply_type') == 'B2B']
        b2cs_data = [r for r in data if r.get('supply_type') == 'B2CS']
        
        b2b_taxable = sum(r.get('taxable_value', 0) for r in b2b_data)
        b2b_igst = sum(r.get('igst', 0) for r in b2b_data)
        b2b_cgst = sum(r.get('cgst', 0) for r in b2b_data)
        b2b_sgst = sum(r.get('sgst', 0) for r in b2b_data)
        
        b2cs_taxable = sum(r.get('taxable_value', 0) for r in b2cs_data)
        b2cs_igst = sum(r.get('igst', 0) for r in b2cs_data)
        b2cs_cgst = sum(r.get('cgst', 0) for r in b2cs_data)
        b2cs_sgst = sum(r.get('sgst', 0) for r in b2cs_data)
        
        return {
            'a_outward_taxable_supplies_other_than_reverse_charge': {
                'taxable_value': round(b2b_taxable, 2),
                'integrated_tax': round(b2b_igst, 2),
                'central_tax': round(b2b_cgst, 2),
                'state_tax': round(b2b_sgst, 2),
                'cess': 0
            },
            'b_outward_taxable_supplies_reverse_charge': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
            'c_outward_non_taxable_supplies': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
            'd_outward_supplies_nongst': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
            'e_others': {'taxable_value': round(b2cs_taxable, 2), 'integrated_tax': round(b2cs_igst, 2),
                        'central_tax': round(b2cs_cgst, 2), 'state_tax': round(b2cs_sgst, 2), 'cess': 0},
            'total_taxable_value': round(b2b_taxable + b2cs_taxable, 2),
            'integrated_tax': round(b2b_igst + b2cs_igst, 2),
            'central_tax': round(b2b_cgst + b2cs_cgst, 2),
            'state_tax': round(b2b_sgst + b2cs_sgst, 2),
            'cess': 0
        }
    
    def _calculate_inter_state(self, data: List[Dict]) -> Dict:
        interstate_data = [r for r in data if r.get('is_interstate', False)]
        unregistered = [r for r in interstate_data if not r.get('customer_gstin')]
        unregistered_taxable = sum(r.get('taxable_value', 0) for r in unregistered)
        unregistered_igst = sum(r.get('igst', 0) for r in unregistered)
        
        return {
            'supplies_made_to_unregistered_persons': {'taxable_value': round(unregistered_taxable, 2), 'integrated_tax': round(unregistered_igst, 2)},
            'supplies_made_to_composition_taxable_persons': {'taxable_value': 0, 'integrated_tax': 0},
            'supplies_made_to_uin_holders': {'taxable_value': 0, 'integrated_tax': 0},
            'state_wise_breakup': []
        }
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {
            'period': self.format_period(period),
            '3_1_tax_on_outward_supplies': {
                'a_outward_taxable_supplies_other_than_reverse_charge': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
                'b_outward_taxable_supplies_reverse_charge': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
                'c_outward_non_taxable_supplies': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
                'd_outward_supplies_nongst': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
                'e_others': {'taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0},
                'total_taxable_value': 0, 'integrated_tax': 0, 'central_tax': 0, 'state_tax': 0, 'cess': 0
            },
            '3_2_inter_state_supplies': {
                'supplies_made_to_unregistered_persons': {'taxable_value': 0, 'integrated_tax': 0},
                'supplies_made_to_composition_taxable_persons': {'taxable_value': 0, 'integrated_tax': 0},
                'supplies_made_to_uin_holders': {'taxable_value': 0, 'integrated_tax': 0},
                'state_wise_breakup': []
            },
            'hsn_summary': [],
            'total_liability': {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0, 'cess': 0}
        }
