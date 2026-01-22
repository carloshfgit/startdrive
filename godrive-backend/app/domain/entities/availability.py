"""
Entidade de Domínio: Availability

Representa a disponibilidade recorrente de um instrutor.
Pura - sem dependências de SQLAlchemy ou FastAPI.
"""
from dataclasses import dataclass
from datetime import time


@dataclass
class AvailabilityEntity:
    """
    Entidade de domínio pura para disponibilidade de instrutor.
    
    Attributes:
        id: Identificador único.
        instructor_id: ID do instrutor.
        day_of_week: Dia da semana (0=Segunda, 6=Domingo).
        start_time: Horário de início.
        end_time: Horário de término.
    """
    id: int
    instructor_id: int
    day_of_week: int  # 0=Monday, 6=Sunday
    start_time: time
    end_time: time

    def is_valid(self) -> bool:
        """Verifica se o horário é válido (início < fim)."""
        return self.start_time < self.end_time
    
    def overlaps_with(self, other: "AvailabilityEntity") -> bool:
        """Verifica se há sobreposição com outra disponibilidade."""
        if self.day_of_week != other.day_of_week:
            return False
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)
