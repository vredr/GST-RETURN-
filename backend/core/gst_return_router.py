"""GST Return Router Module - Universal router for all GST return types"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from gst_engines.gstr1_generator import GSTR1Generator
from gst_engines.gstr3b_generator import GSTR3BGenerator
from gst_engines.gstr9_generator import GSTR9Generator
from gst_engines.gstr4_generator import GSTR4Generator
from gst_engines.gstr6_generator import GSTR6Generator
from gst_engines.gstr7_generator import GSTR7Generator
from gst_engines.gstr8_generator import GSTR8Generator
from gst_engines.gstr2_analyzer import GSTR2Analyzer

logger = logging.getLogger(__name__)

class GSTRouter:
    def __init__(self):
        self.generators = {
            'gstr1': GSTR1Generator(),
            'gstr3b': GSTR3BGenerator(),
            'gstr9': GSTR9Generator(),
            'gstr9c': GSTR9Generator(),
            'gstr4': GSTR4Generator(),
            'gstr6': GSTR6Generator(),
            'gstr7': GSTR7Generator(),
            'gstr8': GSTR8Generator(),
            'gstr2a': GSTR2Analyzer(),
            'gstr2b': GSTR2Analyzer(),
            'gstr5': GSTR1Generator(),
            'gstr10': GSTR1Generator(),
            'gstr11': GSTR1Generator(),
        }
    
    def generate(self, return_type: str, data: List[Dict], period: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        return_type = return_type.lower().replace('-', '').replace('_', '')
        if return_type in ['gstr2a', 'gstr2b']:
            return_type = 'gstr2a'
        elif return_type == 'gstr9c':
            return_type = 'gstr9'
        
        generator = self.generators.get(return_type)
        if not generator:
            raise ValueError(f"Unsupported return type: {return_type}")
        
        logger.info(f"Generating {return_type} with {len(data)} records")
        result = generator.generate(data, period=period, **kwargs)
        result['return_type'] = return_type.upper()
        result['generated_at'] = datetime.utcnow().isoformat()
        result['record_count'] = len(data)
        return result
