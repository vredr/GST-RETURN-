"""GSTR-2A/2B Analyzer - Auto-drafted details of inward supplies"""
from typing import List, Dict, Any, Optional
from collections import defaultdict
from gst_engines.base_generator import BaseGenerator

class GSTR2Analyzer(BaseGenerator):
    def __init__(self):
        super().__init__("GSTR-2A/2B")
    
    def generate(self, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        if not self.validate_data(data):
            return self._empty_return(period)
        
        period = self.format_period(period)
        supplier_wise = self._group_by_supplier(data)
        itc_summary = self._calculate_itc_summary(data)
        actionable = self._identify_actionable(data)
        
        return {
            'period': period,
            'type': 'GSTR-2A',
            'supplier_wise_summary': supplier_wise,
            'itc_summary': itc_summary,
            'actionable_items': actionable,
            'summary': {'total_suppliers': len(supplier_wise), 'total_invoices': len(data),
                       'total_itc_available': itc_summary['total_itc']}
        }
    
    def _group_by_supplier(self, data: List[Dict]) -> List[Dict]:
        grouped = defaultdict(lambda: {'invoices': [], 'total_value': 0, 'total_taxable': 0, 'total_igst': 0,
                                       'total_cgst': 0, 'total_sgst': 0})
        for record in data:
            gstin = record.get('customer_gstin', 'UNREGISTERED')
            grouped[gstin]['invoices'].append({'invoice_number': record.get('invoice_number', ''),
                                               'invoice_date': record.get('invoice_date', ''),
                                               'taxable_value': record.get('taxable_value', 0),
                                               'igst': record.get('igst', 0), 'cgst': record.get('cgst', 0),
                                               'sgst': record.get('sgst', 0), 'total_value': record.get('total_value', 0)})
            grouped[gstin]['total_value'] += record.get('total_value', 0)
            grouped[gstin]['total_taxable'] += record.get('taxable_value', 0)
            grouped[gstin]['total_igst'] += record.get('igst', 0)
            grouped[gstin]['total_cgst'] += record.get('cgst', 0)
            grouped[gstin]['total_sgst'] += record.get('sgst', 0)
        
        return [{'supplier_gstin': gstin, 'invoice_count': len(vals['invoices']),
                 'total_value': round(vals['total_value'], 2), 'total_taxable': round(vals['total_taxable'], 2),
                 'total_igst': round(vals['total_igst'], 2), 'total_cgst': round(vals['total_cgst'], 2),
                 'total_sgst': round(vals['total_sgst'], 2), 'invoices': vals['invoices']}
                for gstin, vals in grouped.items()]
    
    def _calculate_itc_summary(self, data: List[Dict]) -> Dict:
        igst = sum(r.get('igst', 0) for r in data)
        cgst = sum(r.get('cgst', 0) for r in data)
        sgst = sum(r.get('sgst', 0) for r in data)
        return {'igst': round(igst, 2), 'cgst': round(cgst, 2), 'sgst': round(sgst, 2),
                'total_itc': round(igst + cgst + sgst, 2), 'eligible_itc': round(igst + cgst + sgst, 2),
                'ineligible_itc': 0}
    
    def _identify_actionable(self, data: List[Dict]) -> Dict:
        missing_gstin = [r for r in data if not r.get('customer_gstin')]
        high_value = [r for r in data if r.get('total_value', 0) > 100000]
        interstate_b2b = [r for r in data if r.get('is_interstate') and r.get('supply_type') == 'B2B']
        
        return {'missing_gstin': len(missing_gstin), 'high_value_invoices': len(high_value),
                'interstate_b2b': len(interstate_b2b),
                'details': {'missing_gstin_invoices': [{'invoice': r.get('invoice_number'), 'value': r.get('total_value')} for r in missing_gstin[:10]],
                           'high_value_list': [{'invoice': r.get('invoice_number'), 'value': r.get('total_value')} for r in high_value[:10]]}}
    
    def _empty_return(self, period: Optional[str]) -> Dict:
        return {'period': self.format_period(period), 'type': 'GSTR-2A', 'supplier_wise_summary': [],
                'itc_summary': {'igst': 0, 'cgst': 0, 'sgst': 0, 'total_itc': 0, 'eligible_itc': 0, 'ineligible_itc': 0},
                'actionable_items': {'missing_gstin': 0, 'high_value_invoices': 0, 'interstate_b2b': 0,
                                    'details': {'missing_gstin_invoices': [], 'high_value_list': []}},
                'summary': {'total_suppliers': 0, 'total_invoices': 0, 'total_itc_available': 0}}
