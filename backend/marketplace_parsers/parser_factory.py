"""Parser Factory - Creates appropriate parser for each marketplace"""
import logging
from typing import Dict, Type
from marketplace_parsers.base_parser import BaseParser
from marketplace_parsers.meesho_parser import MeeshoParser
from marketplace_parsers.amazon_parser import AmazonParser
from marketplace_parsers.flipkart_parser import FlipkartParser
from marketplace_parsers.shopify_parser import ShopifyParser
from marketplace_parsers.woocommerce_parser import WooCommerceParser
from marketplace_parsers.snapdeal_parser import SnapdealParser
from marketplace_parsers.indiamart_parser import IndiaMartParser
from marketplace_parsers.ajio_parser import AjioParser
from marketplace_parsers.myntra_parser import MyntraParser
from marketplace_parsers.jiomart_parser import JioMartParser
from marketplace_parsers.generic_parser import GenericParser

logger = logging.getLogger(__name__)

class ParserFactory:
    _parsers: Dict[str, Type[BaseParser]] = {
        'meesho': MeeshoParser, 'amazon': AmazonParser, 'flipkart': FlipkartParser,
        'shopify': ShopifyParser, 'woocommerce': WooCommerceParser, 'snapdeal': SnapdealParser,
        'indiamart': IndiaMartParser, 'ajio': AjioParser, 'myntra': MyntraParser,
        'jiomart': JioMartParser, 'generic': GenericParser,
    }
    
    @classmethod
    def get_parser(cls, marketplace: str) -> BaseParser:
        marketplace = marketplace.lower().strip()
        parser_class = cls._parsers.get(marketplace)
        if not parser_class:
            logger.warning(f"No specific parser for {marketplace}, using generic")
            parser_class = GenericParser
        return parser_class()
    
    @classmethod
    def get_supported_marketplaces(cls) -> list:
        return list(cls._parsers.keys())
