# app/schemas/ride.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.infrastructure.db.models.ride import RideStatus

# Input: Criação da reserva (Booking)
class RideCreate(BaseModel):
    instructor_id: int
    scheduled_at: datetime
    # Novos campos obrigatórios para saber onde buscar o aluno
    pickup_latitude: float
    pickup_longitude: float

# Input: Início da aula (O instrutor envia onde ele está)
class RideStart(BaseModel):
    latitude: float
    longitude: float

# Output: Resposta da API
class RideResponse(BaseModel):
    id: int
    student_id: int
    instructor_id: int
    scheduled_at: datetime
    duration_minutes: int
    price: float
    status: RideStatus
    
    # Retornamos para conferência
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None
    
    created_at: datetime

    class Config:
        from_attributes = True