from pydantic import BaseModel
from datetime import time
from typing import List

# O que o Front envia para criar um horário
class AvailabilityCreate(BaseModel):
    day_of_week: int # 0=Segunda, 1=Terça... 6=Domingo
    start_time: time
    end_time: time

# O que a API responde
class AvailabilityResponse(BaseModel):
    id: int
    day_of_week: int
    start_time: time
    end_time: time

    class Config:
        from_attributes = True