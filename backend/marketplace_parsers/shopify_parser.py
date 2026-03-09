"""Shopify Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class ShopifyParser(BaseParser):
    def __init__(self):
        super().__init__("Shopify")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Name', 'name', 'Order ID', 'id', 'Order Number'],
            'invoice_number': ['Name', 'Invoice Number', 'invoice_number', 'Order Name'],
            'invoice_date': ['Created at', 'created_at', 'Date', 'Order Date', 'Processed at'],
            'customer_name': ['Customer Name', 'customer_name', 'Billing Name', 'Shipping Name'],
            'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN', 'Billing GSTIN'],
            'state': ['Billing Province', 'billing_province', 'State', 'Shipping Province', 'Province'],
            'hsn_code': ['HSN', 'hsn', 'HSN Code', 'Lineitem HSN'],
            'tax_rate': ['Tax Rate', 'tax_rate', 'GST Rate', 'Lineitem Tax Rate'],
            'taxable_value': ['Lineitem price', 'lineitem_price', 'Subtotal', 'Lineitem total'],
            'quantity': ['Lineitem quantity', 'lineitem_quantity', 'Quantity', 'Lineitem qty'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Lineitem unit'],
            'total_value': ['Total', 'total', 'Grand Total', 'Total Price']
        }
