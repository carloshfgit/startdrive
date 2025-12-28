# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, login # <--- Importe login

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"]) # <--- Adicione esta linha
api_router.include_router(users.router, prefix="/users", tags=["users"])