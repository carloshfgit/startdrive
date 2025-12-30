from sqlalchemy.orm import Session
from app.models.ride import Ride, RideStatus
from app.schemas.ride import RideCreate

class RideRepository:
    
    def create(self, db: Session, student_id: int, ride_in: RideCreate, price: float):
        """
        Cria a reserva com status PENDING_PAYMENT e preço congelado.
        """
        db_ride = Ride(
            student_id=student_id,
            instructor_id=ride_in.instructor_id,
            scheduled_at=ride_in.scheduled_at,
            price=price, # Preço capturado no momento da reserva
            status=RideStatus.PENDING_PAYMENT,
            duration_minutes=50 # Padrão
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