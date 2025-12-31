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
    
    # Novo campo: Se True, o app deve abrir o modal de avaliação
    has_pending_reviews: bool = False 

    class Config:
        from_attributes = True