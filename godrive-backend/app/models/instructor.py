from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.base import Base

class InstructorProfile(Base):
    __tablename__ = "instructor_profiles"

    # A chave primária é também uma chave estrangeira para users
    # Isso garante a relação 1:1 forte
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    bio = Column(Text, nullable=True)
    hourly_rate = Column(Float, nullable=True)      # Preço da hora/aula
    cnh_category = Column(String, nullable=True)    # Ex: "B", "A", "AD"
    vehicle_model = Column(String, nullable=True)   # Ex: "Gol G5 Branco"
    
    # --- CAMPO MÁGICO DO POSTGIS ---
    # Geometry('POINT', srid=4326) armazena coordenadas GPS (Lat/Lon)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    user = relationship("User", back_populates="instructor_profile")