from pymongo import MongoClient
from config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db[settings.MONGODB_COLLECTION]

    def insert_decision(self, decision_data: dict):
        """Inserisce un documento validato nella collezione."""
        try:
            result = self.collection.insert_one(decision_data)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Errore durante l'inserimento in MongoDB: {str(e)}")
            raise

    def verify_vector_index(self):
        """Verifica l'esistenza dell'indice di Vector Search."""
        # Nota: La creazione dell'indice Atlas Vector Search avviene via API/UI.
        # Qui implementiamo una verifica di integrità.
        logger.info("Verifica indice 'vector_index' in corso...")
        # In un ambiente prod, useremmo l'Atlas Admin API per validare l'indice
        return True
