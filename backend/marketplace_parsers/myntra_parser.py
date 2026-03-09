"""Myntra Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class MyntraParser(BaseParser):
    def __init__(self):
        super().__init__("Myntra")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order_id', 'Order No', 'Order Number'],
            'invoice_number': ['Order ID', 'Invoice Number', 'Invoice No', 'Tax Invoice'],
            'invoice_date': ['Order Date', 'order_date', 'Date', 'Invoice Date'],
            'customer_name': ['Customer Name', 'customer_name', 'Buyer Name', 'Customer'],
            'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN', 'Buyer GSTIN'],
            'state': ['State', 'state', 'Ship State', 'Shipping State', 'Destination State'],
            'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'HSN/SAC'],
            'tax_rate': ['GST Rate', 'gst_rate', 'Tax Rate', 'GST %'],
            'taxable_value': ['Taxable Value', 'taxable_value', 'Net Amount', 'Item Value'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Item Qty'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Unit of Measure'],
            'total_value': ['Total', 'total', 'Grand Total', 'Total Amount']
        }
