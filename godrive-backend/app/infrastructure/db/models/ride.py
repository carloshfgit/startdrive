from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.infrastructure.db.base import Base

class RideStatus(str, enum.Enum):
    PENDING_PAYMENT = "pending_payment" # Aguardando pgto
    SCHEDULED = "scheduled"             # Confirmada/Paga
    IN_PROGRESS = "in_progress"         # Em andamento (Rastreamento ativo)
    COMPLETED = "completed"             # Finalizada com sucesso
    CANCELLED = "cancelled"             # Cancelada (com ou sem multa)

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamentos
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructor_profiles.id"), nullable=False)
    
    # Detalhes do Agendamento
    scheduled_at = Column(DateTime(timezone=True), nullable=False) # Data e Hora de início
    duration_minutes = Column(Integer, default=50) # Aula padrão de 50min
    
    # Financeiro
    price = Column(Float, nullable=False) # Valor cobrado na época
    status = Column(String, default=RideStatus.PENDING_PAYMENT, index=True)
    
    # Auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Navegação
    student = relationship("User", foreign_keys=[student_id], backref="rides_as_student")
    instructor = relationship("InstructorProfile", foreign_keys=[instructor_id], backref="rides_as_instructor")