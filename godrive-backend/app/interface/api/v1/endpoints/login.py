# app/api/v1/endpoints/login.py
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.interface.api import deps
from app.infrastructure.security import security
from app.infrastructure.config.settings import settings
from app.infrastructure.repositories.user_repository import UserRepository
from app.interface.api.schemas.token import Token

router = APIRouter()

@router.post("/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Login OAuth2 compatível. Recebe 'username' (email) e 'password'.
    Retorna o Token de Acesso JWT.
    """
    user_repo = UserRepository()
    # 1. Busca usuário pelo email (form_data.username contém o email)
    user = user_repo.get_by_email(db, email=form_data.username)
    
    # 2. Valida senha
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")

    # 3. Gera e retorna o token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }