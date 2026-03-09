"""Schema Converter Module - Converts marketplace data to standard GST schema"""
import logging
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SchemaConverter:
    GST_SCHEMA_FIELDS = ['invoice_number', 'invoice_date', 'order_id', 'customer_gstin', 'customer_name', 
                         'state', 'state_code', 'hsn_code', 'tax_rate', 'taxable_value', 'cgst', 'sgst', 
                         'igst', 'total_value', 'quantity', 'uqc', 'supply_type', 'is_interstate']
    
    STATE_CODES = {
        'Jammu and Kashmir': '01', 'Himachal Pradesh': '02', 'Punjab': '03', 'Chandigarh': '04',
        'Uttarakhand': '05', 'Haryana': '06', 'Delhi': '07', 'Rajasthan': '08', 'Uttar Pradesh': '09',
        'Bihar': '10', 'Sikkim': '11', 'Arunachal Pradesh': '12', 'Nagaland': '13', 'Manipur': '14',
        'Mizoram': '15', 'Tripura': '16', 'Meghalaya': '17', 'Assam': '18', 'West Bengal': '19',
        'Jharkhand': '20', 'Odisha': '21', 'Chhattisgarh': '22', 'Madhya Pradesh': '23', 'Gujarat': '24',
        'Daman and Diu': '25', 'Dadra and Nagar Haveli': '26', 'Maharashtra': '27', 'Karnataka': '29',
        'Goa': '30', 'Lakshadweep': '31', 'Kerala': '32', 'Tamil Nadu': '33', 'Puducherry': '34',
        'Andaman and Nicobar Islands': '35', 'Telangana': '36', 'Andhra Pradesh': '37', 'Ladakh': '38',
        'Other Territory': '97', 'Centre Jurisdiction': '99'
    }
    
    def __init__(self):
        self.column_mappings = self._load_column_mappings()
    
    def _load_column_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        return {
            'meesho': {
                'order_id': ['Order ID', 'order_id', 'OrderID', 'Order No'],
                'invoice_number': ['Order ID', 'Invoice Number', 'invoice_number', 'Invoice No'],
                'invoice_date': ['Order Date', 'order_date', 'OrderDate', 'Date', 'Purchase Date'],
                'customer_name': ['Customer Name', 'customer_name', 'Buyer Name'],
                'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN', 'Buyer GSTIN'],
                'state': ['Ship State', 'State', 'state', 'Shipping State', 'Destination State'],
                'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'hsn'],
                'tax_rate': ['GST Rate', 'tax_rate', 'Tax Rate', 'GST%', 'gst_rate'],
                'taxable_value': ['Product Price', 'taxable_value', 'Item Price', 'Selling Price', 'Net Amount'],
                'quantity': ['Quantity', 'quantity', 'Qty'],
                'uqc': ['UQC', 'uqc', 'Unit'],
                'total_value': ['Total Value', 'total_value', 'Grand Total']
            },
            'amazon': {
                'order_id': ['Order ID', 'order-id', 'Amazon Order ID'],
                'invoice_number': ['Order ID', 'Invoice Number', 'invoice-id'],
                'invoice_date': ['Purchase Date', 'purchase-date', 'Order Date'],
                'customer_name': ['Buyer Name', 'buyer-name', 'Customer Name'],
                'customer_gstin': ['Buyer GSTIN', 'buyer-gstin', 'GSTIN'],
                'state': ['Ship State', 'ship-state', 'State', 'Shipping State'],
                'hsn_code': ['HSN Code', 'hsn-code', 'HSN'],
                'tax_rate': ['Tax Rate', 'tax-rate', 'GST Rate'],
                'taxable_value': ['Item Price', 'item-price', 'Product Amount'],
                'quantity': ['Quantity', 'quantity', 'Qty'],
                'uqc': ['UQC', 'uqc', 'Unit'],
                'total_value': ['Total', 'total', 'Grand Total']
            },
            'flipkart': {
                'order_id': ['Order ID', 'order_id', 'OrderItemID'],
                'invoice_number': ['Order ID', 'Invoice Number', 'Invoice No'],
                'invoice_date': ['Order Date', 'order_date', 'OrderDate'],
                'customer_name': ['Customer Name', 'customer_name', 'Buyer Name'],
                'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN'],
                'state': ['State', 'state', 'Ship State', 'Shipping State'],
                'hsn_code': ['HSN Code', 'hsn_code', 'HSN'],
                'tax_rate': ['GST Rate', 'gst_rate', 'Tax Rate'],
                'taxable_value': ['Selling Price', 'selling_price', 'Taxable Value', 'Net Amount'],
                'quantity': ['Quantity', 'quantity', 'Qty'],
                'uqc': ['UQC', 'uqc', 'Unit'],
                'total_value': ['Total', 'total', 'Grand Total']
            },
            'shopify': {
                'order_id': ['Name', 'name', 'Order ID', 'id'],
                'invoice_number': ['Name', 'Invoice Number', 'invoice_number'],
                'invoice_date': ['Created at', 'created_at', 'Date'],
                'customer_name': ['Customer Name', 'customer_name', 'Billing Name'],
                'customer_gstin': ['GSTIN', 'gstin', 'Customer GSTIN'],
                'state': ['Billing Province', 'billing_province', 'State'],
                'hsn_code': ['HSN', 'hsn', 'HSN Code'],
                'tax_rate': ['Tax Rate', 'tax_rate', 'GST Rate'],
                'taxable_value': ['Lineitem price', 'lineitem_price', 'Subtotal'],
                'quantity': ['Lineitem quantity', 'lineitem_quantity', 'Quantity'],
                'uqc': ['UQC', 'uqc', 'Unit'],
                'total_value': ['Total', 'total', 'Grand Total']
            },
            'generic': {
                'order_id': ['Order ID', 'order_id', 'Order No', 'Order Number', 'ID'],
                'invoice_number': ['Invoice Number', 'invoice_number', 'Invoice No', 'Bill Number'],
                'invoice_date': ['Invoice Date', 'invoice_date', 'Date', 'Bill Date'],
                'customer_name': ['Customer Name', 'customer_name', 'Buyer Name', 'Party Name'],
                'customer_gstin': ['Customer GSTIN', 'customer_gstin', 'GSTIN', 'Buyer GSTIN'],
                'state': ['State', 'state', 'Place of Supply', 'POS'],
                'hsn_code': ['HSN Code', 'hsn_code', 'HSN', 'HSN/SAC'],
                'tax_rate': ['Tax Rate', 'tax_rate', 'GST Rate', 'Rate'],
                'taxable_value': ['Taxable Value', 'taxable_value', 'Amount', 'Value'],
                'quantity': ['Quantity', 'quantity', 'Qty'],
                'uqc': ['UQC', 'uqc', 'Unit'],
                'total_value': ['Total Value', 'total_value', 'Total', 'Grand Total']
            }
        }
    
    def detect_columns(self, df: pd.DataFrame, marketplace: str) -> Dict[str, str]:
        mappings = self.column_mappings.get(marketplace, self.column_mappings['generic'])
        detected = {}
        df_columns = [str(col).strip() for col in df.columns]
        for standard_field, possible_names in mappings.items():
            for col in df_columns:
                if col in possible_names:
                    detected[standard_field] = col
                    break
        return detected
    
    def convert(self, data: List[Dict], marketplace: str, supplier_state: str = "Maharashtra", supplier_gstin: Optional[str] = None) -> List[Dict]:
        if not data:
            return []
        df = pd.DataFrame(data)
        column_map = self.detect_columns(df, marketplace)
        normalized_data = []
        for idx, row in df.iterrows():
            record = self._normalize_record(row, column_map, supplier_state)
            if record:
                normalized_data.append(record)
        return normalized_data
    
    def _normalize_record(self, row: pd.Series, column_map: Dict[str, str], supplier_state: str) -> Optional[Dict]:
        try:
            record = {}
            record['invoice_number'] = self._get_value(row, column_map.get('invoice_number', ''), '')
            record['order_id'] = self._get_value(row, column_map.get('order_id', ''), record['invoice_number'])
            date_str = self._get_value(row, column_map.get('invoice_date', ''), '')
            record['invoice_date'] = self._parse_date(date_str)
            record['customer_name'] = self._get_value(row, column_map.get('customer_name', ''), '')
            record['customer_gstin'] = self._clean_gstin(self._get_value(row, column_map.get('customer_gstin', ''), ''))
            state = self._get_value(row, column_map.get('state', ''), supplier_state)
            record['state'] = self._normalize_state(state)
            record['state_code'] = self.STATE_CODES.get(record['state'], '97')
            record['hsn_code'] = self._clean_hsn(self._get_value(row, column_map.get('hsn_code', ''), ''))
            tax_rate = self._get_numeric_value(row, column_map.get('tax_rate', ''), 0)
            record['tax_rate'] = tax_rate / 100 if tax_rate > 1 else tax_rate
            record['taxable_value'] = self._get_numeric_value(row, column_map.get('taxable_value', ''), 0)
            record['quantity'] = self._get_numeric_value(row, column_map.get('quantity', ''), 1)
            record['uqc'] = self._get_value(row, column_map.get('uqc', ''), 'PCS')
            record['total_value'] = self._get_numeric_value(row, column_map.get('total_value', ''), record['taxable_value'])
            record['cgst'] = 0
            record['sgst'] = 0
            record['igst'] = 0
            record['supply_type'] = ''
            record['is_interstate'] = record['state'] != supplier_state
            return record
        except Exception as e:
            return None
    
    def classify_transactions(self, data: List[Dict], supplier_state: str) -> List[Dict]:
        B2CL_THRESHOLD = 250000
        for record in data:
            customer_gstin = record.get('customer_gstin', '')
            taxable_value = record.get('taxable_value', 0)
            is_interstate = record.get('is_interstate', False)
            if customer_gstin and len(customer_gstin) == 15:
                record['supply_type'] = 'B2B'
            elif is_interstate and taxable_value > B2CL_THRESHOLD:
                record['supply_type'] = 'B2CL'
            else:
                record['supply_type'] = 'B2CS'
        return data
    
    def calculate_gst(self, data: List[Dict], supplier_state: str) -> List[Dict]:
        for record in data:
            taxable_value = record.get('taxable_value', 0)
            tax_rate = record.get('tax_rate', 0)
            is_interstate = record.get('is_interstate', False)
            if is_interstate:
                record['igst'] = round(taxable_value * tax_rate, 2)
                record['cgst'] = 0
                record['sgst'] = 0
            else:
                half_rate = tax_rate / 2
                record['cgst'] = round(taxable_value * half_rate, 2)
                record['sgst'] = round(taxable_value * half_rate, 2)
                record['igst'] = 0
            record['total_value'] = taxable_value + record['cgst'] + record['sgst'] + record['igst']
        return data
    
    def generate_summary(self, data: List[Dict]) -> Dict:
        if not data:
            return {'total_invoices': 0, 'b2b_count': 0, 'b2cl_count': 0, 'b2cs_count': 0,
                    'total_taxable_value': 0, 'total_cgst': 0, 'total_sgst': 0, 'total_igst': 0, 'total_tax': 0}
        b2b_count = sum(1 for r in data if r.get('supply_type') == 'B2B')
        b2cl_count = sum(1 for r in data if r.get('supply_type') == 'B2CL')
        b2cs_count = sum(1 for r in data if r.get('supply_type') == 'B2CS')
        total_taxable = sum(r.get('taxable_value', 0) for r in data)
        total_cgst = sum(r.get('cgst', 0) for r in data)
        total_sgst = sum(r.get('sgst', 0) for r in data)
        total_igst = sum(r.get('igst', 0) for r in data)
        return {
            'total_invoices': len(data), 'b2b_count': b2b_count, 'b2cl_count': b2cl_count, 'b2cs_count': b2cs_count,
            'total_taxable_value': round(total_taxable, 2), 'total_cgst': round(total_cgst, 2),
            'total_sgst': round(total_sgst, 2), 'total_igst': round(total_igst, 2),
            'total_tax': round(total_cgst + total_sgst + total_igst, 2)
        }
    
    def _get_value(self, row: pd.Series, column: str, default: Any) -> Any:
        if not column:
            return default
        value = row.get(column, default)
        return default if pd.isna(value) else value
    
    def _get_numeric_value(self, row: pd.Series, column: str, default: float) -> float:
        if not column:
            return default
        value = row.get(column, default)
        if pd.isna(value):
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _parse_date(self, date_str: Any) -> str:
        if pd.isna(date_str):
            return datetime.now().strftime('%d-%m-%Y')
        date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', '%d-%b-%Y', '%d-%B-%Y', '%b %d, %Y', '%B %d, %Y']
        for fmt in date_formats:
            try:
                dt = datetime.strptime(str(date_str).strip(), fmt)
                return dt.strftime('%d-%m-%Y')
            except ValueError:
                continue
        return str(date_str)
    
    def _clean_gstin(self, gstin: str) -> str:
        if pd.isna(gstin):
            return ''
        gstin = str(gstin).strip().upper()
        if len(gstin) == 15 and gstin.isalnum():
            return gstin
        return ''
    
    def _clean_hsn(self, hsn: str) -> str:
        if pd.isna(hsn):
            return ''
        hsn = str(hsn).strip()
        if '.' in hsn:
            hsn = hsn.split('.')[0]
        return hsn
    
    def _normalize_state(self, state: str) -> str:
        if pd.isna(state):
            return ''
        state = str(state).strip().title()
        if state in self.STATE_CODES:
            return state
        state_mappings = {'Up': 'Uttar Pradesh', 'Mh': 'Maharashtra', 'Ka': 'Karnataka', 'Tn': 'Tamil Nadu',
                          'Ts': 'Telangana', 'Gj': 'Gujarat', 'Rj': 'Rajasthan', 'Wb': 'West Bengal',
                          'Dl': 'Delhi', 'Hr': 'Haryana', 'Pb': 'Punjab', 'Mp': 'Madhya Pradesh',
                          'Kl': 'Kerala', 'Ap': 'Andhra Pradesh', 'Br': 'Bihar', 'Or': 'Odisha',
                          'Jh': 'Jharkhand', 'Cg': 'Chhattisgarh', 'As': 'Assam', 'Ga': 'Goa'}
        return state_mappings.get(state, state)
