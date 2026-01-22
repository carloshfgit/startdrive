from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship # <--- Import novo
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Novo campo para distinguir tipos (student/instructor)
    user_type = Column(String, default="student", nullable=False) 
    
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento 1 para 1 com o Perfil de Instrutor
    # uselist=False garante que um usuário só tem UM perfil de instrutor
    instructor_profile = relationship("InstructorProfile", back_populates="user", uselist=False)