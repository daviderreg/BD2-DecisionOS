import logging
import requests
from typing import List
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        self.model = settings.EMBEDDING_MODEL
        self.output_dimensionality = 1536 # Valore desiderato
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def generate_embedding(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        try:
            clean_text = " ".join(text.split()).strip()

            if not clean_text:
                return []

            endpoint = f"{self.base_url}/models/{self.model}:embedContent"

            # CORREZIONE QUI: Abbiamo aggiunto 'outputDimensionality' al payload
            payload = {
                "model": self.model, # Alcuni endpoint richiedono il model anche nel body
                "content": {
                    "parts": [
                        {"text": clean_text}
                    ]
                },
                "taskType": task_type,
                "outputDimensionality": self.output_dimensionality # <--- FONDAMENTALE
            }

            params = {"key": self.api_key}

            response = requests.post(
                endpoint,
                params=params,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            return data["embedding"]["values"]

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {response.text}")
            raise RuntimeError(f"AI Embedding HTTP Failure: {e}")

        except Exception as e:
            logger.error(f"Embedding failure: {e}")
            raise RuntimeError(f"AI Embedding Failure: {e}")