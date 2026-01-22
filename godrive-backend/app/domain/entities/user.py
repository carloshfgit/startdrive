"""
Entidade de Domínio: User

Representa um usuário do sistema (aluno ou instrutor).
Pura - sem dependências de SQLAlchemy ou FastAPI.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserEntity:
    """
    Entidade de domínio pura para usuário.
    
    Attributes:
        id: Identificador único do usuário.
        full_name: Nome completo do usuário.
        email: Email único para login.
        user_type: Tipo do usuário ('student' ou 'instructor').
        is_active: Se o usuário está ativo no sistema.
        is_superuser: Se o usuário tem privilégios de admin.
        created_at: Data de criação do registro.
        updated_at: Data da última atualização.
    """
    id: int
    full_name: str
    email: str
    user_type: str = "student"  # "student" | "instructor"
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_instructor(self) -> bool:
        """Verifica se o usuário é um instrutor."""
        return self.user_type == "instructor"
    
    def is_student(self) -> bool:
        """Verifica se o usuário é um aluno."""
        return self.user_type == "student"
    
    def promote_to_instructor(self) -> None:
        """Promove o usuário para instrutor."""
        self.user_type = "instructor"
