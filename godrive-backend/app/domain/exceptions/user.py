"""
Exceções de Domínio: User

Exceções relacionadas a usuários.
Sem dependência de HTTP/FastAPI - puras de domínio.
"""


class UserException(Exception):
    """Exceção base para erros relacionados a usuários."""
    pass


class UserNotFoundException(UserException):
    """Usuário não encontrado no sistema."""
    
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Usuário '{identifier}' não encontrado.")


class UserNotActiveException(UserException):
    """Usuário está inativo."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"Usuário {user_id} está inativo.")


class InsufficientPermissionsException(UserException):
    """Usuário não tem permissões suficientes."""
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
        super().__init__(
            f"Permissão '{required_permission}' requerida para esta ação."
        )
