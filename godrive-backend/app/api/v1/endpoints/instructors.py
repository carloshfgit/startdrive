from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.instructor import InstructorCreate, InstructorResponse
from app.repositories.instructor_repository import InstructorRepository
from app.models.user import User
from app.models.instructor import InstructorProfile # <--- ADICIONE ESTE IMPORT

router = APIRouter()
repo = InstructorRepository()

@router.post("/", response_model=InstructorResponse)
def create_instructor_profile(
    profile_in: InstructorCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Cria ou atualiza o perfil de instrutor do usuário logado.
    """
    # CORREÇÃO AQUI: Usar o MODELO (InstructorProfile), não o repositório
    existing = db.query(InstructorProfile).filter_by(id=current_user.id).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Usuário já possui um perfil de instrutor."
        )
    
    # Atualiza o tipo do usuário para INSTRUCTOR se ainda não for
    if current_user.user_type != "instructor":
        current_user.user_type = "instructor"
        db.add(current_user)
        db.commit()
    
    try:
        new_profile = repo.create(db=db, user_id=current_user.id, profile=profile_in)
        # Injeta o nome do usuário na resposta
        new_profile.full_name = current_user.full_name 
        return new_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar perfil: {str(e)}")

@router.get("/search", response_model=List[InstructorResponse])
def search_instructors(
    latitude: float,
    longitude: float,
    radius: float = Query(10.0, description="Raio de busca em Km"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Busca instrutores próximos num raio de X km.
    """
    instructors = repo.get_by_radius(db, lat=latitude, long=longitude, radius_km=radius)
    return instructors