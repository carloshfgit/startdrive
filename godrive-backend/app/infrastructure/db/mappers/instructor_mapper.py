"""
InstructorMapper

Converte entre InstructorEntity (domínio) e InstructorProfile (SQLAlchemy model).
"""
from typing import Optional

from app.domain.entities.instructor import InstructorEntity
from app.infrastructure.db.models.instructor import InstructorProfile as InstructorModel, InstructorStatus


class InstructorMapper:
    """
    Mapper para conversão bidirecional entre Instructor Entity e Model.
    """
    
    @staticmethod
    def to_entity(model: InstructorModel) -> InstructorEntity:
        """
        Converte um InstructorProfile SQLAlchemy model para InstructorEntity.
        """
        # Extrai status como string
        status_value = model.status.value if hasattr(model.status, 'value') else str(model.status)
        
        # Extrai nome do usuário se disponível
        full_name = model.user.full_name if model.user else None
        
        return InstructorEntity(
            id=model.id,
            user_id=model.id,  # Na arquitetura atual, id = user_id
            latitude=0.0,  # TODO: extrair de location geometry
            longitude=0.0,  # TODO: extrair de location geometry
            hourly_rate=float(model.hourly_rate) if model.hourly_rate else 0.0,
            full_name=full_name,
            vehicle_model=model.vehicle_model,
            vehicle_year=None,  # Não existe no model atual
            status=status_value,
            cnh_url=getattr(model, 'cnh_url', None),
            vehicle_doc_url=getattr(model, 'vehicle_doc_url', None),
        )
    
    @staticmethod
    def to_model(
        entity: InstructorEntity, 
        existing_model: Optional[InstructorModel] = None
    ) -> InstructorModel:
        """
        Converte uma InstructorEntity para InstructorProfile SQLAlchemy model.
        """
        # Mapeia status string para enum
        try:
            model_status = InstructorStatus(entity.status)
        except ValueError:
            model_status = InstructorStatus.PENDING
        
        if existing_model:
            existing_model.hourly_rate = entity.hourly_rate
            existing_model.vehicle_model = entity.vehicle_model
            existing_model.status = model_status
            return existing_model
        
        return InstructorModel(
            id=entity.user_id,
            hourly_rate=entity.hourly_rate,
            vehicle_model=entity.vehicle_model,
            status=model_status,
        )
    
    @staticmethod
    def to_entity_list(models: list[InstructorModel]) -> list[InstructorEntity]:
        """Converte lista de models para lista de entities."""
        return [InstructorMapper.to_entity(m) for m in models]
