"""Amazon Marketplace Parser"""
from marketplace_parsers.base_parser import BaseParser

class AmazonParser(BaseParser):
    def __init__(self):
        super().__init__("Amazon")
    
    def get_column_mapping(self):
        return {
            'order_id': ['Order ID', 'order-id', 'Amazon Order ID', 'OrderItemID'],
            'invoice_number': ['Order ID', 'Invoice Number', 'invoice-id', 'Invoice No'],
            'invoice_date': ['Purchase Date', 'purchase-date', 'Order Date', 'Date'],
            'customer_name': ['Buyer Name', 'buyer-name', 'Customer Name', 'Recipient Name'],
            'customer_gstin': ['Buyer GSTIN', 'buyer-gstin', 'GSTIN', 'Buyer Tax Registration'],
            'state': ['Ship State', 'ship-state', 'State', 'Shipping State', 'Ship To State'],
            'hsn_code': ['HSN Code', 'hsn-code', 'HSN', 'Product Tax Code'],
            'tax_rate': ['Tax Rate', 'tax-rate', 'GST Rate', 'gst-rate', 'Item Tax Rate'],
            'taxable_value': ['Item Price', 'item-price', 'Product Amount', 'Item Total'],
            'quantity': ['Quantity', 'quantity', 'Qty', 'Item Quantity'],
            'uqc': ['UQC', 'uqc', 'Unit', 'Unit of Measure'],
            'total_value': ['Total', 'total', 'Grand Total', 'Order Total']
        }
