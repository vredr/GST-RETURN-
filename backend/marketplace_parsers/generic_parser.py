"""Generic Parser for any Excel/CSV file"""
from marketplace_parsers.base_parser import BaseParser

class GenericParser(BaseParser):
    def __init__(self):
        super().__init__("Generic")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order_id', 'Order No', 'Order Number', 'ID'],
            'invoice_number': ['Invoice Number', 'invoice_number', 'Invoice No', 'Bill Number', 'Bill No'],
            'invoice_date': ['Invoice Date', 'invoice_date', 'Date', 'Bill Date', 'Transaction Date'],
            'customer_name': ['Customer Name', 'customer_name', 'Buyer Name', 'Party Name', 'Client Name'],
            'customer_gstin': ['Customer GSTIN', 'customer_gstin', 'GSTIN', 'Buyer GSTIN', 'Party GSTIN'],
            'state': ['State', 'state', 'Place of Supply', 'POS', 'Supply State'],
            'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'HSN/SAC', 'SAC Code'],
            'tax_rate': ['Tax Rate', 'tax_rate', 'GST Rate', 'Rate', 'GST %'],
            'taxable_value': ['Taxable Value', 'taxable_value', 'Amount', 'Value', 'Net Amount', 'Base Amount'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Item Quantity'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Unit of Measurement', 'UOM'],
            'total_value': ['Total Value', 'total_value', 'Total', 'Grand Total', 'Total Amount']
        }
