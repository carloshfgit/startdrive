from pydantic import BaseModel
from typing import Optional

# Input: Criação do Perfil
class InstructorCreate(BaseModel):
    bio: str
    hourly_rate: float
    cnh_category: str
    vehicle_model: str
    
    # Recebemos lat/long separados do front, e convertemos no backend
    latitude: float
    longitude: float

# Output: Resposta da API
class InstructorResponse(BaseModel):
    id: int
    full_name: str | None = None # Vem do relacionamento com User
    bio: str | None = None
    hourly_rate: float | None = None
    cnh_category: str | None = None
    vehicle_model: str | None = None
    
    # Campo calculado na busca (opcional, pois na criação ele não existe)
    distance: float | None = None 

    class Config:
        from_attributes = True