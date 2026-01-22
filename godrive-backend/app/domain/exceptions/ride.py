"""
Exceções de Domínio: Ride

Exceções relacionadas a aulas de direção.
Sem dependência de HTTP/FastAPI - puras de domínio.
"""


class RideException(Exception):
    """Exceção base para erros relacionados a aulas."""
    pass


class RideNotFoundException(RideException):
    """Aula não encontrada no sistema."""
    
    def __init__(self, ride_id: int):
        self.ride_id = ride_id
        super().__init__(f"Aula com ID {ride_id} não encontrada.")


class RideScheduleInPastException(RideException):
    """Tentativa de agendar aula no passado."""
    
    def __init__(self):
        super().__init__("Não é possível agendar aulas para uma data/hora no passado.")


class SlotNotAvailableException(RideException):
    """Horário solicitado não está disponível."""
    
    def __init__(self, instructor_id: int, requested_time: str):
        self.instructor_id = instructor_id
        self.requested_time = requested_time
        super().__init__(
            f"Instrutor {instructor_id} não está disponível em {requested_time}."
        )


class RideStatusTransitionException(RideException):
    """Transição de status inválida."""
    
    def __init__(self, current_status: str, target_status: str):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(
            f"Não é possível mudar status de '{current_status}' para '{target_status}'."
        )


class UnauthorizedRideActionException(RideException):
    """Usuário não autorizado a realizar ação na aula."""
    
    def __init__(self, action: str, user_id: int, ride_id: int):
        self.action = action
        self.user_id = user_id
        self.ride_id = ride_id
        super().__init__(
            f"Usuário {user_id} não autorizado a {action} a aula {ride_id}."
        )


class RideTooFarToStartException(RideException):
    """Instrutor está muito longe para iniciar a aula."""
    
    def __init__(self, distance_meters: int, max_distance_meters: int):
        self.distance_meters = distance_meters
        self.max_distance_meters = max_distance_meters
        super().__init__(
            f"Você está a {distance_meters}m do aluno. "
            f"Aproxime-se para menos de {max_distance_meters}m para iniciar."
        )
