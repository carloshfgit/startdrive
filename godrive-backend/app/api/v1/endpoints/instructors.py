from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.repositories.availability_repository import AvailabilityRepository
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
availability_repo = AvailabilityRepository()

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

@router.post("/availability", response_model=AvailabilityResponse)
def add_availability(
    availability_in: AvailabilityCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Adiciona um horário recorrente na agenda do instrutor logado.
    """
    # Verifica se é instrutor
    if not current_user.instructor_profile:
        raise HTTPException(status_code=400, detail="Usuário não é um instrutor.")
        
    # TODO: Validar se start_time < end_time
    # TODO: Validar sobreposição de horários (Fase de refinamento)
    
    return availability_repo.create(
        db=db, 
        instructor_id=current_user.instructor_profile.id, 
        availability=availability_in
    )

@router.get("/availability", response_model=List[AvailabilityResponse])
def list_my_availability(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lista todos os horários configurados pelo instrutor logado.
    """
    if not current_user.instructor_profile:
        raise HTTPException(status_code=400, detail="Usuário não é um instrutor.")
        
    return availability_repo.get_by_instructor(db, instructor_id=current_user.instructor_profile.id)