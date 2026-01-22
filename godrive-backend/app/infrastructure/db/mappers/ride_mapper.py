"""
RideMapper

Converte entre RideEntity (domínio) e Ride (SQLAlchemy model).
"""
from typing import Optional
from datetime import datetime

from app.domain.entities.ride import RideEntity, RideStatus as DomainRideStatus
from app.infrastructure.db.models.ride import Ride as RideModel, RideStatus as ModelRideStatus


class RideMapper:
    """
    Mapper para conversão bidirecional entre Ride Entity e Model.
    
    Uso:
        entity = RideMapper.to_entity(model)
        model = RideMapper.to_model(entity)
    """
    
    @staticmethod
    def to_entity(model: RideModel) -> RideEntity:
        """
        Converte um Ride SQLAlchemy model para RideEntity.
        
        Args:
            model: Instância do model SQLAlchemy.
            
        Returns:
            RideEntity de domínio.
        """
        # Mapeia o status do model para o enum de domínio
        status_value = model.status.value if hasattr(model.status, 'value') else str(model.status)
        
        # Tenta mapear para o enum de domínio
        try:
            domain_status = DomainRideStatus(status_value)
        except ValueError:
            # Fallback para PENDING se status não reconhecido
            domain_status = DomainRideStatus.PENDING
        
        return RideEntity(
            id=model.id,
            student_id=model.student_id,
            instructor_id=model.instructor_id,
            scheduled_at=model.scheduled_at,
            price=float(model.price) if model.price else 0.0,
            status=domain_status,
            pickup_latitude=model.pickup_latitude,
            pickup_longitude=model.pickup_longitude,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    @staticmethod
    def to_model(entity: RideEntity, existing_model: Optional[RideModel] = None) -> RideModel:
        """
        Converte uma RideEntity para Ride SQLAlchemy model.
        
        Args:
            entity: Entidade de domínio.
            existing_model: Model existente para atualização (opcional).
            
        Returns:
            Instância do model SQLAlchemy.
        """
        # Mapeia o status de domínio para o enum do model
        try:
            model_status = ModelRideStatus(entity.status.value)
        except ValueError:
            model_status = ModelRideStatus.PENDING_PAYMENT
        
        if existing_model:
            # Atualiza model existente
            existing_model.student_id = entity.student_id
            existing_model.instructor_id = entity.instructor_id
            existing_model.scheduled_at = entity.scheduled_at
            existing_model.price = entity.price
            existing_model.status = model_status
            existing_model.pickup_latitude = entity.pickup_latitude
            existing_model.pickup_longitude = entity.pickup_longitude
            return existing_model
        
        # Cria novo model
        return RideModel(
            id=entity.id if entity.id and entity.id > 0 else None,
            student_id=entity.student_id,
            instructor_id=entity.instructor_id,
            scheduled_at=entity.scheduled_at,
            price=entity.price,
            status=model_status,
            duration_minutes=50,  # Default
            pickup_latitude=entity.pickup_latitude,
            pickup_longitude=entity.pickup_longitude,
        )
    
    @staticmethod
    def to_entity_list(models: list[RideModel]) -> list[RideEntity]:
        """Converte lista de models para lista de entities."""
        return [RideMapper.to_entity(m) for m in models]
