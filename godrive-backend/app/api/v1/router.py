from fastapi import APIRouter
from app.api.v1.endpoints import users, login, instructors, rides, payments, websockets # <--- Adicione websockets

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(instructors.router, prefix="/instructors", tags=["instructors"])
api_router.include_router(rides.router, prefix="/rides", tags=["rides"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
# Adicione esta linha:
api_router.include_router(websockets.router, prefix="/ws", tags=["websockets"])