"""Flipkart Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class FlipkartParser(BaseParser):
    def __init__(self):
        super().__init__("Flipkart")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order_id', 'OrderItemID', 'Order Item ID'],
            'invoice_number': ['Order ID', 'Invoice Number', 'Invoice No', 'Tax Invoice Number'],
            'invoice_date': ['Order Date', 'order_date', 'OrderDate', 'Date', 'Invoice Date'],
            'customer_name': ['Customer Name', 'customer_name', 'Buyer Name', 'Customer'],
            'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN', 'Buyer GSTIN'],
            'state': ['State', 'state', 'Ship State', 'Shipping State', 'Place of Supply'],
            'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'HSN/SAC'],
            'tax_rate': ['GST Rate', 'gst_rate', 'Tax Rate', 'Tax %'],
            'taxable_value': ['Selling Price', 'selling_price', 'Taxable Value', 'Net Amount', 'Item Total'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Item Quantity'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Unit of Measurement'],
            'total_value': ['Total', 'total', 'Grand Total', 'Order Total']
        }
