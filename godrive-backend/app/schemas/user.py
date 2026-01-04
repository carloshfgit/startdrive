from pydantic import BaseModel, EmailStr
from typing import Optional

# O que recebemos na criação (Input)
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

# O que devolvemos para o frontend (Output)
# (NUNCA devolvemos a senha)
class UserResponse(BaseModel):
    id: int
    full_name: str | None = None
    email: EmailStr
    is_active: bool
    has_pending_reviews: bool = False
    
    # 👇 ADICIONE ESTA LINHA
    user_type: str | None = None 

    class Config:
        from_attributes = True