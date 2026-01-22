from sqlalchemy.orm import Session
from app.infrastructure.db.models.availability import Availability
from app.application.dtos import CreateAvailabilityDTO

class AvailabilityRepository:
    
    def create(self, db: Session, instructor_id: int, availability: CreateAvailabilityDTO):
        db_obj = Availability(
            instructor_id=instructor_id,
            day_of_week=availability.day_of_week,
            start_time=availability.start_time,
            end_time=availability.end_time
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_instructor(self, db: Session, instructor_id: int):
        return db.query(Availability)\
                 .filter(Availability.instructor_id == instructor_id)\
                 .order_by(Availability.day_of_week, Availability.start_time)\
                 .all()
                 
    # Opcional: Útil para o instrutor limpar a agenda
    def delete_all_by_instructor(self, db: Session, instructor_id: int):
        db.query(Availability).filter(Availability.instructor_id == instructor_id).delete()
        db.commit()