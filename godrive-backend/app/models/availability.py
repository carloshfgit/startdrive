from sqlalchemy import Column, Integer, ForeignKey, Time, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base import Base

class Availability(Base):
    """
    Define a disponibilidade recorrente do instrutor.
    Ex: Toda Segunda-feira (0) das 08:00 às 12:00.
    """
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, ForeignKey("instructor_profiles.id"), nullable=False)
    
    # 0=Segunda, 1=Terça, ..., 6=Domingo
    day_of_week = Column(SmallInteger, nullable=False) 
    
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relacionamento para acessar dados do instrutor se necessário
    instructor = relationship("InstructorProfile", backref="availabilities")