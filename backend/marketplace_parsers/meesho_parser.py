"""Meesho Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class MeeshoParser(BaseParser):
    def __init__(self):
        super().__init__("Meesho")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order_id', 'OrderID', 'Order No', 'Order Number'],
            'invoice_number': ['Order ID', 'Invoice Number', 'invoice_number', 'Invoice No'],
            'invoice_date': ['Order Date', 'order_date', 'OrderDate', 'Date'],
            'customer_name': ['Customer Name', 'customer_name', 'Buyer Name'],
            'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN', 'Buyer GSTIN'],
            'state': ['Ship State', 'State', 'state', 'Shipping State', 'Destination State'],
            'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'hsn'],
            'tax_rate': ['GST Rate', 'tax_rate', 'Tax Rate', 'GST%', 'gst_rate'],
            'taxable_value': ['Product Price', 'taxable_value', 'Item Price', 'Selling Price', 'Net Amount'],
            'quantity': ['Quantity', 'quantity', 'Qty'],
            'uqc': ['UQC', 'uqc', 'Unit'],
            'total_value': ['Total Value', 'total_value', 'Grand Total']
        }
