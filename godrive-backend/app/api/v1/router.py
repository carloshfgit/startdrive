from fastapi import APIRouter
from app.api.v1.endpoints import (
    users, login, instructors, rides, 
    payments, websockets, admin, reviews, 
    courses, quizzes
)
api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(instructors.router, prefix="/instructors", tags=["instructors"])
api_router.include_router(rides.router, prefix="/rides", tags=["rides"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(websockets.router, prefix="/ws", tags=["websockets"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"]) 
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])