"""
Adapter: InstructorRepositoryAdapter

Adapta o InstructorRepository existente para implementar a interface IInstructorRepository.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.instructor import InstructorEntity
from app.domain.interfaces.instructor_repository import IInstructorRepository
from app.infrastructure.db.models.instructor import InstructorProfile
from app.infrastructure.repositories.instructor_repository import InstructorRepository


class InstructorRepositoryAdapter:
    """
    Adapter que envolve o InstructorRepository legado.
    
    Implementa a interface IInstructorRepository do domain layer.
    """
    
    def __init__(self, db: Session):
        self._db = db
        self._repo = InstructorRepository()
    
    def _model_to_entity(self, model: InstructorProfile) -> InstructorEntity:
        """Converte modelo SQLAlchemy para entidade de domínio."""
        return InstructorEntity(
            id=model.id,
            user_id=model.id,  # Na arquitetura atual, id = user_id
            latitude=0.0,  # TODO: extrair do geometry
            longitude=0.0,  # TODO: extrair do geometry
            hourly_rate=model.hourly_rate or 0.0,
            full_name=model.user.full_name if model.user else None,
            vehicle_model=model.vehicle_model,
            vehicle_year=None,  # Não existe no modelo atual
            status=model.status.value if hasattr(model.status, 'value') else str(model.status),
            cnh_url=model.cnh_url if hasattr(model, 'cnh_url') else None,
            vehicle_doc_url=model.vehicle_doc_url if hasattr(model, 'vehicle_doc_url') else None,
        )
    
    def get_by_id(self, instructor_id: int) -> Optional[InstructorEntity]:
        """Busca instrutor por ID."""
        model = self._db.query(InstructorProfile).filter(
            InstructorProfile.id == instructor_id
        ).first()
        if model:
            return self._model_to_entity(model)
        return None
    
    def get_by_user_id(self, user_id: int) -> Optional[InstructorEntity]:
        """Busca instrutor pelo ID do usuário."""
        # Na arquitetura atual, instructor_id = user_id
        return self.get_by_id(user_id)
    
    def get_by_radius(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float
    ) -> List[InstructorEntity]:
        """Busca instrutores por raio geográfico."""
        results = self._repo.get_by_radius(self._db, lat, lng, radius_km)
        # O método legado retorna dicts, não modelos
        entities = []
        for result in results:
            entities.append(InstructorEntity(
                id=result['id'],
                user_id=result['id'],
                latitude=lat,  # Aproximação
                longitude=lng,  # Aproximação  
                hourly_rate=result.get('hourly_rate', 0.0),
                full_name=result.get('full_name'),
                vehicle_model=result.get('vehicle_model'),
                status="approved",  # Assumindo aprovado se retornado
            ))
        return entities
    
    def create(self, instructor: InstructorEntity) -> InstructorEntity:
        """Cria um novo perfil de instrutor."""
        # Delega para o método legado
        raise NotImplementedError("Use InstructorRepository.create diretamente por enquanto")
    
    def update(self, instructor: InstructorEntity) -> InstructorEntity:
        """Atualiza um perfil de instrutor."""
        raise NotImplementedError("Use InstructorRepository.update_status diretamente por enquanto")
