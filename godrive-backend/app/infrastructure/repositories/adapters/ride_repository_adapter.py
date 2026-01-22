"""
Adapter: RideRepositoryAdapter

Adapta o RideRepository existente para implementar a interface IRideRepository.
Permite usar o repositório legado enquanto respeita Clean Architecture.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.ride import RideEntity, RideStatus as DomainRideStatus
from app.domain.interfaces.ride_repository import IRideRepository
from app.infrastructure.db.models.ride import Ride, RideStatus as ModelRideStatus
from app.infrastructure.repositories.ride_repository import RideRepository


class RideRepositoryAdapter:
    """
    Adapter que envolve o RideRepository legado.
    
    Implementa a interface IRideRepository do domain layer,
    convertendo entre entidades de domínio e modelos SQLAlchemy.
    """
    
    def __init__(self, db: Session):
        self._db = db
        self._repo = RideRepository()
    
    def _model_to_entity(self, model: Ride) -> RideEntity:
        """Converte modelo SQLAlchemy para entidade de domínio."""
        return RideEntity(
            id=model.id,
            student_id=model.student_id,
            instructor_id=model.instructor_id,
            scheduled_at=model.scheduled_at,
            price=model.price,
            status=DomainRideStatus(model.status.value if hasattr(model.status, 'value') else model.status),
            pickup_latitude=model.pickup_latitude,
            pickup_longitude=model.pickup_longitude,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def create(self, ride: RideEntity) -> RideEntity:
        """Persiste uma nova aula."""
        # Cria diretamente no banco para evitar dependência de RideCreate schema
        db_ride = Ride(
            student_id=ride.student_id,
            instructor_id=ride.instructor_id,
            scheduled_at=ride.scheduled_at,
            price=ride.price,
            status=ModelRideStatus.PENDING_PAYMENT,
            duration_minutes=50,
            pickup_latitude=ride.pickup_latitude,
            pickup_longitude=ride.pickup_longitude,
        )
        self._db.add(db_ride)
        self._db.commit()
        self._db.refresh(db_ride)
        return self._model_to_entity(db_ride)
    
    def get_by_id(self, ride_id: int) -> Optional[RideEntity]:
        """Busca aula por ID."""
        model = self._repo.get_by_id(self._db, ride_id)
        if model:
            return self._model_to_entity(model)
        return None
    
    def get_by_student(self, student_id: int) -> List[RideEntity]:
        """Lista aulas de um aluno."""
        models = self._repo.get_by_student(self._db, student_id)
        return [self._model_to_entity(m) for m in models]
    
    def get_by_instructor(self, instructor_id: int) -> List[RideEntity]:
        """Lista aulas de um instrutor."""
        models = self._repo.get_by_instructor(self._db, instructor_id)
        return [self._model_to_entity(m) for m in models]
    
    def update(self, ride: RideEntity) -> RideEntity:
        """Atualiza uma aula existente."""
        model = self._db.query(Ride).filter(Ride.id == ride.id).first()
        if model:
            model.status = ModelRideStatus(ride.status.value)
            model.pickup_latitude = ride.pickup_latitude
            model.pickup_longitude = ride.pickup_longitude
            self._db.commit()
            self._db.refresh(model)
            return self._model_to_entity(model)
        raise ValueError(f"Ride {ride.id} não encontrada")
