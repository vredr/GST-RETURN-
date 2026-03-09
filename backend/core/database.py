"""Database module for TaxNow GST Platform"""
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from core.config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
    
    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            self.db = self.client[settings.DATABASE_NAME]
            await self.db.raw_data.create_index("upload_id", unique=True)
            await self.db.processed_data.create_index("upload_id", unique=True)
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
    
    async def disconnect(self):
        if self.client:
            self.client.close()
    
    async def health_check(self) -> str:
        try:
            await self.client.admin.command('ping')
            return "connected"
        except:
            return "disconnected"
    
    async def store_raw_data(self, upload_id: str, marketplace: str, data: List[Dict], business_id: Optional[str] = None):
        document = {
            "upload_id": upload_id,
            "marketplace": marketplace,
            "business_id": business_id,
            "data": data,
            "record_count": len(data),
            "created_at": datetime.utcnow(),
            "status": "uploaded"
        }
        await self.db.raw_data.insert_one(document)
    
    async def get_raw_data(self, upload_id: str) -> Optional[Dict]:
        return await self.db.raw_data.find_one({"upload_id": upload_id})
    
    async def store_processed_data(self, upload_id: str, data: List[Dict]):
        document = {
            "upload_id": upload_id,
            "data": data,
            "record_count": len(data),
            "processed_at": datetime.utcnow(),
            "status": "processed"
        }
        await self.db.processed_data.update_one({"upload_id": upload_id}, {"$set": document}, upsert=True)
    
    async def get_processed_data(self, upload_id: str) -> Optional[Dict]:
        return await self.db.processed_data.find_one({"upload_id": upload_id})
