from pydantic import BaseModel
from datetime import datetime
from app.models.ride import RideStatus

# Input: Aluno diz "Com quem" e "Quando"
class RideCreate(BaseModel):
    instructor_id: int
    scheduled_at: datetime
    # duration_minutes é opcional, assumiremos 50min padrão na lógica

# Output: Detalhes da reserva
class RideResponse(BaseModel):
    id: int
    student_id: int
    instructor_id: int
    scheduled_at: datetime
    duration_minutes: int
    price: float
    status: RideStatus
    created_at: datetime

    class Config:
        from_attributes = True