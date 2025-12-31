from sqlalchemy.orm import Session
from app.models.ride import Ride, RideStatus
from app.schemas.ride import RideCreate
from sqlalchemy import extract, cast, Date
from datetime import date

class RideRepository:
    
    def create(self, db: Session, student_id: int, ride_in: RideCreate, price: float):
        db_ride = Ride(
            student_id=student_id,
            instructor_id=ride_in.instructor_id,
            scheduled_at=ride_in.scheduled_at,
            price=price,
            status=RideStatus.PENDING_PAYMENT,
            duration_minutes=50,
            # Mapeando os novos campos
            pickup_latitude=ride_in.pickup_latitude,
            pickup_longitude=ride_in.pickup_longitude
        )
        db.add(db_ride)
        db.commit()
        db.refresh(db_ride)
        return db_ride

    def get_by_student(self, db: Session, student_id: int):
        return db.query(Ride).filter(Ride.student_id == student_id).order_by(Ride.scheduled_at.desc()).all()

    def get_by_instructor(self, db: Session, instructor_id: int):
        return db.query(Ride).filter(Ride.instructor_id == instructor_id).order_by(Ride.scheduled_at.desc()).all()
    
    def get_by_id(self, db: Session, ride_id: int):
        return db.query(Ride).filter(Ride.id == ride_id).first()
    
    def get_by_instructor_and_date(self, db: Session, instructor_id: int, date_filter: date):
        """
        Busca todas as aulas de um instrutor que ocorrem em uma data específica (ano-mes-dia).
        """
        return db.query(Ride).filter(
            Ride.instructor_id == instructor_id,
            # Faz o cast do campo DateTime para Date para comparar apenas o dia
            cast(Ride.scheduled_at, Date) == date_filter
        ).all()