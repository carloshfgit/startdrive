# app/api/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.config import settings
from app.schemas.token import TokenPayload
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Define que o token deve vir no header: "Authorization: Bearer <token>"
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

# Dependência para pegar a sessão do banco (já usamos no endpoint de users)
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Dependência crítica: Valida o Token e retorna o Usuário Atual
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
        )
        
    user_repo = UserRepository()
    user = user_repo.get_by_email(db, email=token_data.sub)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="O usuário não tem privilégios suficientes (Admin Required)"
        )
    return current_user