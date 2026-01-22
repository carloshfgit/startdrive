"""
Interface: IRideRepository

Protocol para o repositório de aulas.
Define o contrato sem implementação concreta.
"""
from typing import Protocol, List, Optional
from datetime import datetime

from app.domain.entities.ride import RideEntity


class IRideRepository(Protocol):
    """
    Interface para o repositório de aulas.
    
    Implementações concretas devem estar em infrastructure/repositories/.
    """
    
    def create(self, ride: RideEntity) -> RideEntity:
        """
        Persiste uma nova aula.
        
        Args:
            ride: Entidade de aula a ser persistida.
            
        Returns:
            A entidade com ID preenchido.
        """
        ...
    
    def get_by_id(self, ride_id: int) -> Optional[RideEntity]:
        """
        Busca uma aula por ID.
        
        Args:
            ride_id: ID da aula.
            
        Returns:
            Entidade da aula ou None se não encontrada.
        """
        ...
    
    def get_by_student(self, student_id: int) -> List[RideEntity]:
        """
        Lista todas as aulas de um aluno.
        
        Args:
            student_id: ID do aluno.
            
        Returns:
            Lista de aulas do aluno.
        """
        ...
    
    def get_by_instructor(self, instructor_id: int) -> List[RideEntity]:
        """
        Lista todas as aulas de um instrutor.
        
        Args:
            instructor_id: ID do instrutor.
            
        Returns:
            Lista de aulas do instrutor.
        """
        ...
    
    def update(self, ride: RideEntity) -> RideEntity:
        """
        Atualiza uma aula existente.
        
        Args:
            ride: Entidade com dados atualizados.
            
        Returns:
            Entidade atualizada.
        """
        ...
