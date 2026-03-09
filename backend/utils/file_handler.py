"""File Handler Utility"""
import os
import logging
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from core.config import settings

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.output_dir = Path(settings.OUTPUT_DIR)
        self._ensure_directories()
    
    def _ensure_directories(self):
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_upload(self, file: UploadFile, upload_id: str) -> str:
        try:
            filename = file.filename or "upload.xlsx"
            extension = Path(filename).suffix
            file_path = self.upload_dir / f"{upload_id}{extension}"
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            logger.info(f"Saved upload to {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Error saving upload: {e}")
            raise
    
    def cleanup(self, file_path: str):
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"Cleaned up {file_path}")
        except Exception as e:
            logger.warning(f"Error cleaning up file: {e}")
    
    def health_check(self) -> str:
        try:
            test_file = self.upload_dir / ".health_check"
            test_file.touch()
            test_file.unlink()
            return "healthy"
        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            return "unhealthy"
    
    def get_output_path(self, filename: str) -> str:
        return str(self.output_dir / filename)
