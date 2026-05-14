# © 2026 DecisionOS - Tutti i diritti riservati.
from fastapi import FastAPI, HTTPException, Query, Depends, status
from typing import List
from datetime import datetime

from config import settings
from models import DecisionCardCreate, DecisionCardUpdate, DecisionCardResponse
from database_service import DatabaseService
from vector_service import VectorService

app = FastAPI(
    title="DecisionOS - Memory Engine API",
    description="API per la gestione del ciclo di vita delle Decision Cards",
    version="2.0.0"
)

# Dependency Injection per i servizi
db_service = DatabaseService()
vector_service = VectorService()

@app.post("/decisions", response_model=DecisionCardResponse, status_code=status.HTTP_201_CREATED)
async def create_decision(payload: DecisionCardCreate):
    """
    Crea una nuova Decision Card.
    Genera automaticamente l'embedding basandosi su decisione_finale e motivazione.
    """
    # 1. Generazione Embedding
    text_to_embed = f"{payload.decisione_finale} {payload.motivazione}"
    embedding = vector_service.generate_embedding(text_to_embed)
    
    # 2. Preparazione Documento
    doc_data = payload.model_dump()
    doc_data.update({
        "embedding": embedding,
        "timestamp": datetime.utcnow()
    })
    
    # 3. Salvataggio
    inserted_id = db_service.create_decision(doc_data)
    doc_data["_id"] = inserted_id
    return doc_data

@app.get("/decisions", response_model=List[DecisionCardResponse])
async def list_decisions(
    limit: int = Query(10, ge=1, le=100), 
    offset: int = Query(0, ge=0)
):
    """Recupera l'elenco delle decisioni con paginazione."""
    return db_service.get_decisions(limit, offset)

@app.get("/decisions/{id}", response_model=DecisionCardResponse)
async def get_decision(id: str):
    """Recupera una singola decisione tramite ID."""
    doc = db_service.get_decision_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Decision Card non trovata")
    return doc

@app.put("/decisions/{id}", response_model=DecisionCardResponse)
async def update_decision(id: str, payload: DecisionCardUpdate):
    """
    Aggiorna una Decision Card. 
    Rigenera l'embedding solo se 'decisione_finale' o 'motivazione' sono stati modificati.
    """
    existing_doc = db_service.get_decision_by_id(id)
    if not existing_doc:
        raise HTTPException(status_code=404, detail="Decision Card non trovata")
    
    update_data = payload.model_dump(exclude_unset=True)
    
    # Logica di Sincronizzazione Embedding
    text_fields = ["decisione_finale", "motivazione"]
    needs_reembedding = any(field in update_data for field in text_fields)
    
    if needs_reembedding:
        # Calcola il nuovo testo combinando i nuovi valori con quelli esistenti
        new_decision = update_data.get("decisione_finale", existing_doc.get("decisione_finale"))
        new_motivation = update_data.get("motivazione", existing_doc.get("motivazione"))
        
        text_to_embed = f"{new_decision} {new_motivation}"
        update_data["embedding"] = vector_service.generate_embedding(text_to_embed)
        update_data["timestamp"] = datetime.utcnow() # Aggiorna timestamp all'editing

    updated_doc = db_service.update_decision(id, update_data)
    return updated_doc

@app.delete("/decisions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_decision(id: str):
    """Rimuove permanentemente una Decision Card."""
    success = db_service.delete_decision(id)
    if not success:
        raise HTTPException(status_code=404, detail="Decision Card non trovata")
    return None