"""GSTR-6 Generator - Return for Input Service Distributors (ISD)"""
from typing import List, Dict, Any, Optional
from collections import defaultdict
from gst_engines.base_generator import BaseGenerator

class GSTR6Generator(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-6")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        itc_received = self._calculate_itc_received(data)
        isd_distribution = self._calculate_isd_distribution(data)
        
        return {
            'period': period,
            '3_itc_received': itc_received,
            '4_isd_distribution': isd_distribution,
            '5_re_distribution': {'redistribution_of_itc': 0, 'reversal_of_itc': 0},
            'summary': {'total_itc_received': itc_received['total_itc'], 'total_itc_distributed': isd_distribution['total_distributed']}
        }
    
    def _calculate_itc_received(self, data: List[Dict]) -> Dict:
        igst = sum(r.get('igst', 0) for r in data)
        cgst = sum(r.get('cgst', 0) for r in data)
        sgst = sum(r.get('sgst', 0) for r in data)
        
        return {
            'from_registered_suppliers': {'igst': round(igst, 2), 'cgst': round(cgst, 2), 'sgst': round(sgst, 2)},
            'from_unregistered_suppliers': {'igst': 0, 'cgst': 0, 'sgst': 0},
            'import_of_goods': {'igst': 0, 'cgst': 0, 'sgst': 0},
            'import_of_services': {'igst': 0, 'cgst': 0, 'sgst': 0},
            'total_itc': round(igst + cgst + sgst, 2)
        }
    
    def _calculate_isd_distribution(self, data: List[Dict]) -> Dict:
        state_wise = defaultdict(lambda: {'igst': 0, 'cgst': 0, 'sgst': 0})
        for record in data:
            state = record.get('state_code', '97')
            state_wise[state]['igst'] += record.get('igst', 0)
            state_wise[state]['cgst'] += record.get('cgst', 0)
            state_wise[state]['sgst'] += record.get('sgst', 0)
        
        distributions = []
        total_distributed = 0
        for state, values in state_wise.items():
            dist_total = values['igst'] + values['cgst'] + values['sgst']
            total_distributed += dist_total
            distributions.append({'gstin_of_unit': f"XX{state}XXXXXXXXX", 'unit_name': f"Unit {state}",
                                  'igst': round(values['igst'], 2), 'cgst': round(values['cgst'], 2),
                                  'sgst': round(values['sgst'], 2), 'total': round(dist_total, 2)})
        
        return {'distributions': distributions, 'total_distributed': round(total_distributed, 2)}
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {
            'period': self.format_period(period),
            '3_itc_received': {'from_registered_suppliers': {'igst': 0, 'cgst': 0, 'sgst': 0},
                               'from_unregistered_suppliers': {'igst': 0, 'cgst': 0, 'sgst': 0},
                               'import_of_goods': {'igst': 0, 'cgst': 0, 'sgst': 0},
                               'import_of_services': {'igst': 0, 'cgst': 0, 'sgst': 0}, 'total_itc': 0},
            '4_isd_distribution': {'distributions': [], 'total_distributed': 0},
            '5_re_distribution': {'redistribution_of_itc': 0, 'reversal_of_itc': 0},
            'summary': {'total_itc_received': 0, 'total_itc_distributed': 0}
        }
