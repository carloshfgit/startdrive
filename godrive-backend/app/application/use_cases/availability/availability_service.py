from datetime import date, datetime, timedelta, time
from typing import List

from sqlalchemy.orm import Session

from app.infrastructure.db.models.ride import RideStatus
from app.infrastructure.repositories.availability_repository import AvailabilityRepository
from app.infrastructure.repositories.ride_repository import RideRepository

class AvailabilityService:
    def __init__(self):
        self.availability_repo = AvailabilityRepository()
        self.ride_repo = RideRepository()

    def get_available_slots(
        self, 
        db: Session, 
        instructor_id: int, 
        query_date: date
    ) -> List[time]:
        """
        Calcula os horários disponíveis (slots de 1h) para um instrutor em uma data específica.
        Lógica: (Disponibilidade Recorrente) - (Aulas Marcadas/Pagas)
        """
        
        # 1. Identifica o dia da semana da data solicitada (0=Segunda, 6=Domingo)
        day_of_week = query_date.weekday()

        # 2. Busca a regra de disponibilidade do instrutor para esse dia
        # (Estou usando o método que busca tudo e filtrando em memória pois são poucos registros)
        all_availabilities = self.availability_repo.get_by_instructor(db, instructor_id)
        daily_rule = next((a for a in all_availabilities if a.day_of_week == day_of_week), None)

        if not daily_rule:
            return []  # Instrutor não trabalha neste dia da semana

        # 3. Gera os "Slots Candidatos" (Horários possíveis baseados na regra)
        # Ex: Se trabalha das 08:00 às 12:00 -> [08:00, 09:00, 10:00, 11:00]
        candidate_slots = []
        
        # Criamos datas dummy apenas para poder somar horas
        current_dt = datetime.combine(query_date, daily_rule.start_time)
        end_dt = datetime.combine(query_date, daily_rule.end_time)
        
        # Loop de 1 em 1 hora
        while current_dt + timedelta(hours=1) <= end_dt:
            candidate_slots.append(current_dt.time())
            current_dt += timedelta(hours=1)
            
        # Se não houver slots gerados (ex: horário muito curto), retorna vazio
        if not candidate_slots:
            return []

        # 4. Busca as aulas já agendadas para esse dia (Ocupadas)
        # Precisamos de um método novo no repo para filtrar por data exata
        booked_rides = self.ride_repo.get_by_instructor_and_date(db, instructor_id, query_date)

        # 5. Filtra os horários ocupados
        # Ignoramos aulas canceladas (RideStatus.CANCELLED)
        busy_times = set()
        for ride in booked_rides:
            if ride.status != RideStatus.CANCELLED:
                # Extrai apenas a hora da aula agendada
                busy_times.add(ride.scheduled_at.time())

        # 6. Subtração: Remove os horários ocupados da lista de candidatos
        final_slots = [
            slot for slot in candidate_slots 
            if slot not in busy_times
        ]

        return sorted(final_slots)