# app/api/v1/endpoints/admin.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.interface.api import deps
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.instructor import InstructorStatus
from app.interface.api.schemas.instructor import InstructorResponse
from app.infrastructure.repositories.instructor_repository import InstructorRepository

router = APIRouter()
instructor_repo = InstructorRepository()

@router.get("/instructors/pending", response_model=List[InstructorResponse])
def list_pending_instructors(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser) # Apenas Admin
):
    """
    Lista todos os instrutores aguardando aprovação.
    """
    return instructor_repo.get_pending(db)

@router.patch("/instructors/{instructor_id}/approve")
def approve_instructor(
    instructor_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    Aprova um instrutor, permitindo que ele apareça nas buscas.
    """
    instructor = instructor_repo.update_status(db, instructor_id, InstructorStatus.VERIFIED)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    
    return {"message": f"Instrutor {instructor.id} aprovado com sucesso!"}

@router.patch("/instructors/{instructor_id}/reject")
def reject_instructor(
    instructor_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    instructor = instructor_repo.update_status(db, instructor_id, InstructorStatus.REJECTED)
    return {"message": "Instrutor rejeitado."}