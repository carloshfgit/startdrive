from app.interface.api.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.infrastructure.repositories.availability_repository import AvailabilityRepository
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session
from app.interface.api import deps
from app.interface.api.schemas.instructor import InstructorCreate, InstructorResponse
from app.infrastructure.repositories.instructor_repository import InstructorRepository
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.instructor import InstructorProfile # <--- ADICIONE ESTE IMPORT
from datetime import date, time # <--- Importe 'date' e 'time'
from app.application.use_cases.availability.availability_service import AvailabilityService # <--- Importe o Serviço
import shutil
import os
from fastapi import File, UploadFile
from fastapi_cache.decorator import cache
from typing import List, Optional
from app.application.dtos import CreateInstructorDTO, CreateAvailabilityDTO

router = APIRouter()
repo = InstructorRepository()
availability_repo = AvailabilityRepository()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- FUNÇÃO HELPER PARA O CACHE ---
def search_key_builder(
    func,
    namespace: Optional[str] = "",
    _request: Request = None,  # Adicionei o _
    _response: Response = None, # Adicionei o _
    *args,
    **kwargs,
):
    """
    Gera uma chave de cache única baseada APENAS na lat, long e radius.
    Ignora 'db' e 'current_user' para não quebrar o Redis.
    """
    lat = kwargs.get("latitude")
    lon = kwargs.get("longitude")
    rad = kwargs.get("radius")
    
    # Ex: godrive-cache:search:-23.55:-46.63:10.0
    return f"godrive-cache:search:{lat}:{lon}:{rad}"

@router.post("/me/documents")
def upload_documents(
    cnh_file: UploadFile = File(None),
    vehicle_file: UploadFile = File(None),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Upload de CNH e Documento do Veículo.
    Salva localmente e atualiza URLs no perfil.
    """
    if not current_user.instructor_profile:
        raise HTTPException(status_code=400, detail="Perfil de instrutor não encontrado.")

    cnh_url = None
    vehicle_url = None

    # Função auxiliar simples para salvar
    def save_file(file: UploadFile, prefix: str):
        file_path = f"{UPLOAD_DIR}/{prefix}_{current_user.id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    if cnh_file:
        cnh_url = save_file(cnh_file, "CNH")
    
    if vehicle_file:
        vehicle_url = save_file(vehicle_file, "VEHICLE")

    repo.update_documents(db, current_user.id, cnh_url, vehicle_url)
    
    return {"message": "Documentos enviados com sucesso. Aguarde aprovação."}

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
        # Converte Pydantic Schema para DTO (Clean Architecture)
        instructor_dto = CreateInstructorDTO(
            bio=profile_in.bio,
            hourly_rate=profile_in.hourly_rate,
            cnh_category=profile_in.cnh_category,
            vehicle_model=profile_in.vehicle_model,
            latitude=profile_in.latitude,
            longitude=profile_in.longitude,
        )
        new_profile = repo.create(db=db, user_id=current_user.id, profile=instructor_dto)
        # Injeta o nome do usuário na resposta
        new_profile.full_name = current_user.full_name 
        return new_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar perfil: {str(e)}")

@router.get("/search", response_model=List[InstructorResponse])
@cache(expire=60, key_builder=search_key_builder) # <--- USAMOS O BUILDER AQUI
def search_instructors(
    latitude: float,
    longitude: float,
    radius: float = Query(10.0, description="Raio de busca em Km"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Busca instrutores próximos num raio de X km.
    (Cacheado por 1 minuto no Redis)
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
    
    # Converte Pydantic Schema para DTO (Clean Architecture)
    availability_dto = CreateAvailabilityDTO(
        day_of_week=availability_in.day_of_week,
        start_time=availability_in.start_time,
        end_time=availability_in.end_time,
    )
    
    return availability_repo.create(
        db=db, 
        instructor_id=current_user.instructor_profile.id, 
        availability=availability_dto
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

@router.get("/{instructor_id}/availability", response_model=List[time])
def get_instructor_availability_slots(
    instructor_id: int,
    date: date = Query(..., description="Data para consultar disponibilidade (YYYY-MM-DD)"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retorna os horários calculados (slots) disponíveis para um instrutor em uma data específica.
    Exemplo de uso: /instructors/1/availability?date=2024-12-30
    """
    service = AvailabilityService()
    available_slots = service.get_available_slots(db=db, instructor_id=instructor_id, query_date=date)
    
    return available_slots