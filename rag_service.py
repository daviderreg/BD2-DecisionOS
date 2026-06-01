import logging
import google.generativeai as genai
from typing import List, Dict, Any, Tuple
from config import settings
from search_service import SearchService

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Configurazione Gemini per la generazione testuale
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # UTILIZZIAMO IL MODELLO ESATTO DALLA TUA LISTA
        # Questo modello è ottimizzato per la velocità e l'efficienza RAG
        self.model = genai.GenerativeModel('models/gemini-2.5-flash') 
        
        self.search_service = SearchService()

    def _assemble_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Trasforma i documenti MongoDB in un blocco di testo strutturato per l'AI.
        """
        if not documents:
            return "Nessun documento pertinente trovato."
        
        context_blocks = []
        for doc in documents:
            block = (
                f"ID: {doc['_id']}\n"
                f"TITOLO: {doc.get('titolo', 'N/A')}\n"
                f"DECISIONE: {doc.get('decisione_finale', 'N/A')}\n"
                f"MOTIVAZIONE: {doc.get('motivazione', 'N/A')}\n"
                f"-------------------"
            )
            context_blocks.append(block)
        
        return "\n\n".join(context_blocks)

    def generate_answer(self, question: str) -> Tuple[str, List[str]]:
        """
        Flusso RAG: Search -> Context Assembly -> LLM Generation.
        """
        try:
            # 1. Retrieval: Trova i documenti più simili
            relevant_docs = self.search_service.semantic_search(question, top_k=3)
            
            if not relevant_docs:
                return "Informazione non presente nei log decisionali.", []

            # 2. Augmentation: Costruisce il contesto
            context = self._assemble_context(relevant_docs)
            source_ids = [str(doc['_id']) for doc in relevant_docs]

            # 3. Generation: Prompting rigoroso
            system_prompt = (
                "Sei l'Assistente di Memoria Aziendale. Il tuo compito è rispondere a domande "
                "tecniche basandoti sui documenti forniti nel contesto. \n\n"
                "REGOLE DI RISPOSTA:\n"
                "1. Utilizza le informazioni contenute nel contesto per costruire la risposta.\n"
                "2. Se l'informazione è presente ma espressa in modo diverso, usa il tuo ragionamento "
                "per collegare i fatti e rispondere in modo naturale.\n"
                "3. Se e SOLO SE l'informazione è totalmente assente dal contesto, rispondi esattamente: "
                "'Informazione non presente nei log decisionali'.\n"
                "4. Cita sempre gli ID delle decisioni utilizzate (es: [ID: 65...]).\n"
                "5. Sii tecnico, conciso e obiettivo.\n\n"
                f"CONTESTO:\n{context}\n\n"
                f"DOMANDA: {question}\n\n"
                "RISPOSTA:"
            )

            response = self.model.generate_content(system_prompt)
            
            return response.text, source_ids

        except Exception as e:
            logger.error(f"Errore nella pipeline RAG: {str(e)}")
            raise RuntimeError(f"RAG Generation Failure: {e}")