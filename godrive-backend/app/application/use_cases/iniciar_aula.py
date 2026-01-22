"""
Use Case: Iniciar Aula

Caso de uso para instrutor iniciar uma aula agendada.
Valida geofencing e status da aula.
"""
from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.interfaces.ride_repository import IRideRepository
from app.domain.exceptions.ride import (
    RideNotFoundException,
    RideStatusTransitionException,
    UnauthorizedRideActionException,
    RideTooFarToStartException,
)


@dataclass
class IniciarAulaInput:
    """Dados de entrada para iniciar aula."""
    ride_id: int
    instructor_user_id: int
    current_latitude: float
    current_longitude: float


@dataclass
class IniciarAulaOutput:
    """Dados de saída após iniciar aula."""
    ride: RideEntity


class IniciarAulaUseCase:
    """
    Caso de Uso: Iniciar uma aula agendada.
    
    Regras de Negócio:
    1. A aula deve existir
    2. Apenas o instrutor responsável pode iniciar
    3. A aula deve estar com status SCHEDULED
    4. O instrutor deve estar próximo ao local de encontro (150m)
    """
    
    # Tolerância de distância em metros
    MAX_DISTANCE_METERS = 150
    
    def __init__(self, ride_repository: IRideRepository):
        self._ride_repo = ride_repository
    
    def execute(self, input_data: IniciarAulaInput) -> IniciarAulaOutput:
        # 1. Buscar aula
        ride = self._ride_repo.get_by_id(input_data.ride_id)
        if not ride:
            raise RideNotFoundException(input_data.ride_id)
        
        # 2. Verificar autorização
        if ride.instructor_id != input_data.instructor_user_id:
            raise UnauthorizedRideActionException(
                action="iniciar",
                user_id=input_data.instructor_user_id,
                ride_id=input_data.ride_id
            )
        
        # 3. Verificar status
        if not ride.can_be_started():
            raise RideStatusTransitionException(
                current_status=ride.status.value,
                target_status=RideStatus.IN_PROGRESS.value
            )
        
        # 4. Verificar geofencing (se local de encontro definido)
        if ride.pickup_latitude and ride.pickup_longitude:
            distance = self._calculate_distance(
                ride.pickup_latitude, ride.pickup_longitude,
                input_data.current_latitude, input_data.current_longitude
            )
            if distance > self.MAX_DISTANCE_METERS:
                raise RideTooFarToStartException(
                    distance_meters=int(distance),
                    max_distance_meters=self.MAX_DISTANCE_METERS
                )
        
        # 5. Iniciar aula
        ride.start()
        updated_ride = self._ride_repo.update(ride)
        
        return IniciarAulaOutput(ride=updated_ride)
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula distância em metros usando fórmula de Haversine.
        """
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Raio da Terra em metros
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
