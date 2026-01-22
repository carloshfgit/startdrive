"""
Entidade de Domínio: Instructor

Representa o perfil de um instrutor de direção.
Pura - sem dependências de SQLAlchemy ou FastAPI.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class InstructorEntity:
    """
    Entidade de domínio pura para perfil de instrutor.
    
    Attributes:
        id: Identificador único do perfil.
        user_id: ID do usuário associado.
        full_name: Nome completo (desnormalizado para performance).
        latitude: Latitude da localização do instrutor.
        longitude: Longitude da localização do instrutor.
        hourly_rate: Valor da hora/aula.
        vehicle_model: Modelo do veículo.
        vehicle_year: Ano do veículo.
        status: Status de aprovação (pending/approved/suspended).
        cnh_url: URL do documento CNH.
        vehicle_doc_url: URL do documento do veículo.
    """
    id: int
    user_id: int
    latitude: float
    longitude: float
    hourly_rate: float = 0.0
    full_name: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    status: str = "pending"  # "pending" | "approved" | "suspended"
    cnh_url: Optional[str] = None
    vehicle_doc_url: Optional[str] = None

    def is_approved(self) -> bool:
        """Verifica se o instrutor está aprovado."""
        return self.status == "approved"
    
    def is_pending(self) -> bool:
        """Verifica se o instrutor está pendente de aprovação."""
        return self.status == "pending"
    
    def approve(self) -> None:
        """Aprova o instrutor."""
        self.status = "approved"
    
    def suspend(self) -> None:
        """Suspende o instrutor."""
        self.status = "suspended"
