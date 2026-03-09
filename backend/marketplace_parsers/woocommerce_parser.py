"""WooCommerce Parser"""
from marketplace_parsers.base_parser import BaseParser

class WooCommerceParser(BaseParser):
    def __init__(self):
        super().__init__("WooCommerce")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order_id', 'ID', 'Order Number'],
            'invoice_number': ['Order ID', 'Invoice Number', 'Invoice No', 'Invoice ID'],
            'invoice_date': ['Order Date', 'order_date', 'Date', 'Created Date', 'Post Date'],
            'customer_name': ['Billing First Name', 'billing_first_name', 'Customer Name', 'Billing Name'],
            'customer_gstin': ['GSTIN', 'gstin', '_billing_gstin', 'Customer GSTIN', 'Billing GSTIN'],
            'state': ['Billing State', 'billing_state', 'State', 'Shipping State'],
            'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'Product HSN'],
            'tax_rate': ['Tax Rate', 'tax_rate', 'GST Rate', 'Item Tax Rate'],
            'taxable_value': ['Item Total', 'item_total', 'Subtotal', 'Line Total', 'Product Total'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Item Quantity'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Product Unit'],
            'total_value': ['Order Total', 'order_total', 'Total', 'Grand Total']
        }
