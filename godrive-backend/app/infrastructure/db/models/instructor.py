from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, Enum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.infrastructure.db.base import Base
import enum

class InstructorStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class InstructorProfile(Base):
    __tablename__ = "instructor_profiles"

    # A chave primária é também uma chave estrangeira para users
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    bio = Column(Text, nullable=True)
    hourly_rate = Column(Float, nullable=True)
    cnh_category = Column(String, nullable=True)
    vehicle_model = Column(String, nullable=True)
    
    # Geometry('POINT', srid=4326) armazena coordenadas GPS (Lat/Lon)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    # --- CORREÇÃO AQUI ---
    # Adicionamos 'values_callable' para garantir que o SQLAlchemy use "pending" e não "PENDING"
    status = Column(
        Enum(
            InstructorStatus, 
            values_callable=lambda x: [e.value for e in x]
        ), 
        default=InstructorStatus.PENDING, 
        nullable=False
    )
    
    cnh_url = Column(String, nullable=True)
    vehicle_doc_url = Column(String, nullable=True)
    
    # Campo novo (migração 5f50b...) - Adicione se não estiver no seu arquivo local ainda
    stripe_account_id = Column(String, nullable=True, unique=True)

    user = relationship("User", back_populates="instructor_profile")