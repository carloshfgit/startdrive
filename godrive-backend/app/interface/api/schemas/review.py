# app/schemas/review.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

# Input: O que o front envia
class ReviewCreate(BaseModel):
    ride_id: int
    rating: int = Field(..., ge=1, le=5, description="Nota de 1 a 5")
    comment: Optional[str] = None

# Output: O que a API responde
class ReviewResponse(BaseModel):
    id: int
    ride_id: int
    reviewer_id: int
    reviewee_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    
    # Podemos incluir o nome de quem avaliou para exibir na lista
    reviewer_name: Optional[str] = None

    class Config:
        from_attributes = True

# Output para Média (usado no perfil do instrutor)
class RatingSummary(BaseModel):
    average: float
    count: int