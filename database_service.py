from pymongo import MongoClient, ReturnDocument
from config import settings
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db[settings.MONGODB_COLLECTION]

    def create_decision(self, data: dict):
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            logger.error(f"DB Error - Create: {str(e)}")
            raise

    def get_decisions(self, limit: int, offset: int):
        try:
            cursor = self.collection.find().skip(offset).limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"DB Error - Get All: {str(e)}")
            raise

    def get_decision_by_id(self, decision_id: str):
        try:
            return self.collection.find_one({"_id": ObjectId(decision_id)})
        except Exception as e:
            logger.error(f"DB Error - Get by ID: {str(e)}")
            raise

    def update_decision(self, decision_id: str, update_data: dict):
        try:
            # find_one_and_update restituisce il documento aggiornato
            return self.collection.find_one_and_update(
                {"_id": ObjectId(decision_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )
        except Exception as e:
            logger.error(f"DB Error - Update: {str(e)}")
            raise

    def delete_decision(self, decision_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(decision_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"DB Error - Delete: {str(e)}")
            raise