"""IndiaMART Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class IndiaMartParser(BaseParser):
    def __init__(self):
        super().__init__("IndiaMART")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order_id', 'Enquiry ID', 'RFQ ID'],
            'invoice_number': ['Order ID', 'Invoice Number', 'Invoice No', 'Proforma Invoice'],
            'invoice_date': ['Order Date', 'order_date', 'Date', 'Enquiry Date'],
            'customer_name': ['Buyer Name', 'buyer_name', 'Customer Name', 'Company Name'],
            'customer_gstin': ['Buyer GST', 'buyer_gst', 'GSTIN', 'Buyer GSTIN'],
            'state': ['Buyer State', 'buyer_state', 'State', 'Buyer Location'],
            'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'Product HSN'],
            'tax_rate': ['GST Rate', 'gst_rate', 'Tax Rate', 'GST %'],
            'taxable_value': ['Product Value', 'product_value', 'Taxable Value', 'Item Value'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Order Quantity'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Unit of Measurement'],
            'total_value': ['Order Value', 'order_value', 'Total', 'Total Amount']
        }
