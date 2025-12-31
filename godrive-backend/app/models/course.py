from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    cover_image_url = Column(String, nullable=True)
    is_published = Column(Boolean, default=False) # Rascunho ou Publicado
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    modules = relationship("Module", backref="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", backref="course")


class Module(Base):
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    order = Column(Integer, default=0) # Para ordenar 1, 2, 3...

    # Relacionamentos
    lessons = relationship("Lesson", backref="module", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "course_lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=False)
    title = Column(String, nullable=False)
    video_url = Column(String, nullable=True) # Link do YouTube/Vimeo/S3
    duration_seconds = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())
    price_paid = Column(Float, nullable=False) # Registra quanto foi pago na época

    user = relationship("User", backref="enrollments")

    # Regra: Um usuário só pode se matricular uma vez no mesmo curso
    __table_args__ = (
        UniqueConstraint('user_id', 'course_id', name='uq_enrollment_user_course'),
    )