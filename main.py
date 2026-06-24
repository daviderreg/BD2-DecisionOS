# © 2026 DecisionOS - Tutti i diritti riservati.
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from bson import ObjectId

from config import settings
from models import DecisionCardCreate, DecisionCardUpdate, DecisionCardResponse
from database_service import DatabaseService
from vector_service import VectorService
from rag_service import RAGService # Import del nuovo servizio RAG
from pydantic import BaseModel

app = FastAPI(
    title="DecisionOS - Memory Engine API",
    description="API per la gestione del ciclo di vita delle Decision Cards e Interrogazione Semantica (RAG)",
    version="3.0.0"
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependency Injection ---
db_service = DatabaseService()
vector_service = VectorService()
rag_service = RAGService()

# --- Helper di Serializzazione ---
def format_mongo_doc(doc):
    """Converte l'ObjectId di MongoDB in stringa per evitare errori 500 in FastAPI"""
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

# --- Modelli per l'endpoint /ask ---
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: List[str]

# ==========================================
# ENDPOINTS CRUD (Milestone 2)
# ==========================================

@app.post("/decisions", response_model=DecisionCardResponse, status_code=status.HTTP_201_CREATED)
async def create_decision(payload: DecisionCardCreate):
    try:
        text_to_embed = f"{payload.decisione_finale} {payload.motivazione}"
        embedding = vector_service.generate_embedding(text_to_embed)
        
        doc_data = payload.model_dump()
        doc_data.update({
            "embedding": embedding,
            "timestamp": datetime.utcnow()
        })
        
        inserted_id = db_service.create_decision(doc_data)
        doc_data["_id"] = str(inserted_id) # <--- CRITICO: conversione in stringa
        return doc_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/decisions", response_model=List[DecisionCardResponse])
async def list_decisions(
    limit: int = Query(100, ge=1, le=100), 
    offset: int = Query(0, ge=0)
):
    docs = db_service.get_decisions(limit, offset)
    return [format_mongo_doc(doc) for doc in docs] # <--- Blindato

@app.get("/decisions/{id}", response_model=DecisionCardResponse)
async def get_decision(id: str):
    doc = db_service.get_decision_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Decision Card non trovata")
    return format_mongo_doc(doc) # <--- Blindato

@app.put("/decisions/{id}", response_model=DecisionCardResponse)
async def update_decision(id: str, payload: DecisionCardUpdate):
    existing_doc = db_service.get_decision_by_id(id)
    if not existing_doc:
        raise HTTPException(status_code=404, detail="Decision Card non trovata")
    
    update_data = payload.model_dump(exclude_unset=True)
    
    text_fields = ["decisione_finale", "motivazione"]
    needs_reembedding = any(field in update_data for field in text_fields)
    
    if needs_reembedding:
        new_decision = update_data.get("decisione_finale", existing_doc.get("decisione_finale"))
        new_motivation = update_data.get("motivazione", existing_doc.get("motivazione"))
        text_to_embed = f"{new_decision} {new_motivation}"
        update_data["embedding"] = vector_service.generate_embedding(text_to_embed)
        update_data["timestamp"] = datetime.utcnow()

    updated_doc = db_service.update_decision(id, update_data)
    return format_mongo_doc(updated_doc) # <--- Blindato

@app.delete("/decisions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_decision(id: str):
    success = db_service.delete_decision(id)
    if not success:
        raise HTTPException(status_code=404, detail="Decision Card non trovata")
    return None

# ==========================================
# ENDPOINT RAG (Milestone 3)
# ==========================================

@app.post("/ask", response_model=AskResponse)
async def ask_dss(payload: AskRequest):
    """
    Endpoint di interrogazione semantica. 
    Utilizza la pipeline RAG per rispondere basandosi sulla memoria aziendale.
    """
    try:
        answer, sources = rag_service.generate_answer(payload.question)
        return AskResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
