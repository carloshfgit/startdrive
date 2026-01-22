"""
Interface: IAvailabilityService

Protocol para o serviço de disponibilidade de instrutores.
Define o contrato sem implementação concreta.
"""
from typing import Protocol, List
from datetime import date, time


class IAvailabilityService(Protocol):
    """
    Interface para o serviço de disponibilidade.
    
    Implementações concretas devem estar em infrastructure/services/.
    """
    
    def get_available_slots(
        self, 
        instructor_id: int, 
        query_date: date
    ) -> List[time]:
        """
        Retorna os horários disponíveis de um instrutor em uma data.
        
        Args:
            instructor_id: ID do instrutor.
            query_date: Data para consultar disponibilidade.
            
        Returns:
            Lista de horários disponíveis (time objects).
        """
        ...
