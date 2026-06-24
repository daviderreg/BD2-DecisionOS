from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# Helper per gestire la conversione ObjectId <-> String di MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.str_schema(),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x)),
        )

class AlternativeScartata(BaseModel):
    opzione: str
    motivo_scarto: str

class DecisionCardBase(BaseModel):
    titolo: str = Field(..., min_length=3, max_length=255)
    decisione_finale: str = Field(..., min_length=3)
    motivazione: str = Field(..., min_length=3)
    alternative_scartate: List[AlternativeScartata] = []
    decisori: List[str] = []
    tags: List[str] = []
    parent_id: Optional[str] = None

class DecisionCardCreate(DecisionCardBase):
    """Schema per l'inserimento di una nuova decisione (POST)"""
    pass

class DecisionCardUpdate(BaseModel):
    """Schema per l'aggiornamento (PUT) - Tutti i campi opzionali"""
    titolo: Optional[str] = None
    decisione_finale: Optional[str] = None
    motivazione: Optional[str] = None
    alternative_scartate: Optional[List[AlternativeScartata]] = None
    decisori: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    parent_id: Optional[str] = None

class DecisionCardResponse(DecisionCardBase):
    """Schema per la risposta API (GET) - Include ID e Timestamp"""
    id: PyObjectId = Field(alias="_id")
    timestamp: datetime
    embedding: Optional[List[float]] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)