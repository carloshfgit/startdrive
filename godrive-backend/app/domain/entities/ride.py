"""
Entidade de Domínio: Ride

Representa uma aula de direção agendada.
Pura - sem dependências de SQLAlchemy ou FastAPI.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class RideStatus(str, Enum):
    """Status possíveis de uma aula."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class RideEntity:
    """
    Entidade de domínio pura para aula de direção.
    
    Attributes:
        id: Identificador único da aula.
        student_id: ID do aluno.
        instructor_id: ID do instrutor.
        scheduled_at: Data/hora agendada para a aula.
        price: Valor da aula.
        status: Status atual da aula.
        pickup_latitude: Latitude do ponto de encontro.
        pickup_longitude: Longitude do ponto de encontro.
        created_at: Data de criação.
        updated_at: Última atualização.
    """
    id: int
    student_id: int
    instructor_id: int
    scheduled_at: datetime
    price: float
    status: RideStatus = RideStatus.PENDING
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def can_be_started(self) -> bool:
        """Verifica se a aula pode ser iniciada."""
        return self.status == RideStatus.SCHEDULED
    
    def can_be_finished(self) -> bool:
        """Verifica se a aula pode ser finalizada."""
        return self.status == RideStatus.IN_PROGRESS
    
    def can_be_cancelled(self) -> bool:
        """Verifica se a aula pode ser cancelada."""
        return self.status in (RideStatus.PENDING, RideStatus.SCHEDULED)
    
    def start(self) -> None:
        """Inicia a aula."""
        if not self.can_be_started():
            raise ValueError(f"Não é possível iniciar uma aula com status '{self.status}'.")
        self.status = RideStatus.IN_PROGRESS
        self.updated_at = datetime.now(timezone.utc)
    
    def finish(self) -> None:
        """Finaliza a aula."""
        if not self.can_be_finished():
            raise ValueError(f"Não é possível finalizar uma aula com status '{self.status}'.")
        self.status = RideStatus.COMPLETED
        self.updated_at = datetime.now(timezone.utc)
    
    def cancel(self) -> None:
        """Cancela a aula."""
        if not self.can_be_cancelled():
            raise ValueError(f"Não é possível cancelar uma aula com status '{self.status}'.")
        self.status = RideStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)
