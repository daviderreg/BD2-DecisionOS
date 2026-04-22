from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class AlternativeScartata(BaseModel):
    opzione: str
    motivo_scarto: str

class DecisionCard(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    titolo: str
    decisione_finale: str
    motivazione: str
    alternative_scartate: List[AlternativeScartata]
    decisori: List[str]
    timestamp: datetime
    parent_id: Optional[str] = None  # Supporta ObjectId o String per branching
    tags: List[str]
    embedding: Optional[List[float]] = Field(default=None, description="Vector representation of the decision")

    def to_mongodb(self):
        """Converte il modello Pydantic in un dizionario compatibile con MongoDB."""
        data = self.model_dump()
        # Gestione parent_id per compatibilità ObjectId
        if self.parent_id and len(self.parent_id) == 24:
            data['parent_id'] = ObjectId(self.parent_id)
        return data
