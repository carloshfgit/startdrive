"""
Exceções de Domínio: Instructor

Exceções relacionadas a instrutores.
Sem dependência de HTTP/FastAPI - puras de domínio.
"""


class InstructorException(Exception):
    """Exceção base para erros relacionados a instrutores."""
    pass


class InstructorNotFoundException(InstructorException):
    """Instrutor não encontrado no sistema."""
    
    def __init__(self, instructor_id: int):
        self.instructor_id = instructor_id
        super().__init__(f"Instrutor com ID {instructor_id} não encontrado.")


class InstructorNotApprovedException(InstructorException):
    """Instrutor não está aprovado para dar aulas."""
    
    def __init__(self, instructor_id: int):
        self.instructor_id = instructor_id
        super().__init__(
            f"Instrutor {instructor_id} não está aprovado para dar aulas."
        )


class InstructorProfileAlreadyExistsException(InstructorException):
    """Usuário já possui um perfil de instrutor."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"Usuário {user_id} já possui um perfil de instrutor.")
