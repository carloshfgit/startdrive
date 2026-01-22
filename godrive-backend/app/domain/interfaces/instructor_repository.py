"""
Interface: IInstructorRepository

Protocol para o repositório de instrutores.
Define o contrato sem implementação concreta.
"""
from typing import Protocol, List, Optional

from app.domain.entities.instructor import InstructorEntity


class IInstructorRepository(Protocol):
    """
    Interface para o repositório de instrutores.
    
    Implementações concretas devem estar em infrastructure/repositories/.
    """
    
    def get_by_id(self, instructor_id: int) -> Optional[InstructorEntity]:
        """
        Busca um instrutor por ID.
        
        Args:
            instructor_id: ID do instrutor.
            
        Returns:
            Entidade do instrutor ou None se não encontrado.
        """
        ...
    
    def get_by_user_id(self, user_id: int) -> Optional[InstructorEntity]:
        """
        Busca um instrutor pelo ID do usuário.
        
        Args:
            user_id: ID do usuário associado.
            
        Returns:
            Entidade do instrutor ou None.
        """
        ...
    
    def get_by_radius(
        self, 
        lat: float, 
        lng: float, 
        radius_km: float
    ) -> List[InstructorEntity]:
        """
        Busca instrutores dentro de um raio geográfico.
        
        Args:
            lat: Latitude do ponto central.
            lng: Longitude do ponto central.
            radius_km: Raio de busca em quilômetros.
            
        Returns:
            Lista de instrutores dentro do raio.
        """
        ...
    
    def create(self, instructor: InstructorEntity) -> InstructorEntity:
        """
        Cria um novo perfil de instrutor.
        
        Args:
            instructor: Entidade do instrutor.
            
        Returns:
            Entidade com ID preenchido.
        """
        ...
    
    def update(self, instructor: InstructorEntity) -> InstructorEntity:
        """
        Atualiza um perfil de instrutor.
        
        Args:
            instructor: Entidade com dados atualizados.
            
        Returns:
            Entidade atualizada.
        """
        ...
