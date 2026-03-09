"""Snapdeal Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class SnapdealParser(BaseParser):
    def __init__(self):
        super().__init__("Snapdeal")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order Code', 'order_code', 'Order ID', 'Suborder Code'],
            'invoice_number': ['Order Code', 'Invoice Number', 'Invoice No', 'Tax Invoice No'],
            'invoice_date': ['Order Date', 'order_date', 'Date', 'Invoice Date'],
            'customer_name': ['Customer Name', 'customer_name', 'Buyer Name', 'Customer'],
            'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN', 'Buyer GSTIN'],
            'state': ['State', 'state', 'Ship State', 'Shipping State', 'Destination State'],
            'hsn_code': ['HSN', 'hsn', 'HSN Code', 'HSN/SAC'],
            'tax_rate': ['GST Rate', 'gst_rate', 'Tax Rate', 'GST %'],
            'taxable_value': ['Net Amt', 'net_amt', 'Taxable Value', 'Item Value'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Item Qty'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Unit of Measure'],
            'total_value': ['Total', 'total', 'Grand Total', 'Total Amount']
        }
