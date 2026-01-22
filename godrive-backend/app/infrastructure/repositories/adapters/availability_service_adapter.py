"""
Adapter: AvailabilityServiceAdapter

Adapta o AvailabilityService existente para implementar a interface IAvailabilityService.
"""
from typing import List
from datetime import date, time
from sqlalchemy.orm import Session

from app.domain.interfaces.availability_service import IAvailabilityService
from app.application.use_cases.availability.availability_service import AvailabilityService


class AvailabilityServiceAdapter:
    """
    Adapter que envolve o AvailabilityService legado.
    
    Implementa a interface IAvailabilityService do domain layer.
    """
    
    def __init__(self, db: Session):
        self._db = db
        self._service = AvailabilityService()
    
    def get_available_slots(
        self, 
        instructor_id: int, 
        query_date: date
    ) -> List[time]:
        """Retorna os horários disponíveis de um instrutor em uma data."""
        return self._service.get_available_slots(
            db=self._db,
            instructor_id=instructor_id,
            query_date=query_date
        )
