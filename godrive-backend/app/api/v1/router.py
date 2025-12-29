from fastapi import APIRouter
from app.api.v1.endpoints import users, login, instructors # <--- Importe instructors

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# Adicione esta linha:
api_router.include_router(instructors.router, prefix="/instructors", tags=["instructors"])