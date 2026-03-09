"""Base Parser for all marketplace parsers"""
import logging
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class BaseParser(ABC):
    def __init__(self, marketplace_name: str):
        self.marketplace_name = marketplace_name
    
    def parse(self, file_path: str) -> List[Dict]:
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path, dtype=str)
            else:
                df = pd.read_excel(file_path, dtype=str)
            
            df.columns = [str(col).strip() for col in df.columns]
            df = df.dropna(how='all')
            data = df.to_dict('records')
            
            logger.info(f"Parsed {len(data)} records from {self.marketplace_name}")
            return data
        except Exception as e:
            logger.error(f"Error parsing {self.marketplace_name} file: {e}")
            raise
    
    @abstractmethod
    def get_column_mapping(self) -> Dict[str, List[str]]:
        pass
