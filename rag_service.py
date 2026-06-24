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
        self.model = genai.GenerativeModel('gemini-2.5-flash') 
        
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

            # 3. Generation: Prompting in modalità "Analista"
            system_prompt = (
                "Sei l'Analista della Memoria Aziendale. Il tuo obiettivo è estrarre ogni possibile dettaglio "
                "tecnico dai documenti forniti per rispondere alla domanda dell'utente.\n\n"
                "REGOLE DI OPERAZIONE:\n"
                "1. AGNOSI DEL RISULTATO: Non dare risposte binarie. Se trovi informazioni correlate, riportale tutte, "
                "anche se non rispondono perfettamente alla domanda. L'utente preferisce un'informazione parziale "
                "che pertinente a un silenzio assoluto.\n"
                "2. SINTESI TECNICA: Se l'informazione è distribuita su più documenti, uniscili in un'unica spiegazione "
                "coerente e tecnica.\n"
                "3. TRASPARENZA: Se l'informazione è parziale, scrivi: 'Sulla base dei log disponibili, posso dirti che... [info], "
                "ma non trovo dettagli specifici su [cosa manca]'.\n"
                "4. CITAZIONI OBBLIGATORIE: Ogni affermazione DEVE essere supportata dall'ID del documento (es: [ID: 65...]).\n"
                "5. STILE: Sii estremamente tecnico, conciso e obiettivo.\n\n"
                f"CONTESTO RECUPERATO:\n{context}\n\n"
                f"DOMANDA DELL'UTENTE: {question}\n\n"
                "ANALISI TECNICA:"
            )

            # LOG DI DEBUG: Stampa il contesto per capire cosa vede l'AI
            print("\n" + "="*50 + "\nDEBUG RAG CONTEXT\n" + "="*50)
            print(f"QUERY: {question}")
            print(f"CONTEXT:\n{context}")
            print("="*50 + "\n")

            response = self.model.generate_content(system_prompt)
            
            return response.text, source_ids

        except Exception as e:
            logger.error(f"Errore nella pipeline RAG: {str(e)}")
            raise RuntimeError(f"RAG Generation Failure: {e}")