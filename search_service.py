import logging
from typing import List, Dict, Any
from database_service import DatabaseService
from vector_service import VectorService

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.vector_service = VectorService()

    def semantic_search(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Esegue una ricerca vettoriale su MongoDB Atlas per trovare 
        i documenti più simili semanticamente alla query.
        """
        try:
            # 1. Generazione embedding della query
            query_vector = self.vector_service.generate_embedding(query_text)

            # 2. Pipeline di aggregazione Atlas Vector Search
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index", # Nome indice configurato in M1
                        "path": "embedding",     # Campo dove risiedono i vettori
                        "queryVector": query_vector,
                        "numCandidates": 100,    # Numero di candidati per l'algoritmo ANN
                        "limit": top_k           # Numero finale di risultati da restituire
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "titolo": 1,
                        "decisione_finale": 1,
                        "motivazione": 1,
                        "score": {"$meta": "vectorSearchScore"} # Recupero del punteggio di similarità
                    }
                }
            ]

            # Esecuzione della query di aggregazione
            results = list(self.db_service.collection.aggregate(pipeline))
            logger.info(f"Ricerca semantica completata. Trovati {len(results)} documenti.")
            return results

        except Exception as e:
            logger.error(f"Errore durante la ricerca semantica: {str(e)}")
            raise RuntimeError(f"Semantic Search Failure: {e}")