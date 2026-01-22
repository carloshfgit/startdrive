# app/models/review.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.db.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento com a Aula
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    
    # Quem avaliou e Quem foi avaliado
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Nota (1 a 5) e Comentário
    rating = Column(Integer, nullable=False) 
    comment = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    ride = relationship("Ride", backref="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    reviewee = relationship("User", foreign_keys=[reviewee_id], backref="received_reviews")

    # Regra de Banco: Um usuário só pode avaliar uma aula UMA vez
    __table_args__ = (
        UniqueConstraint('ride_id', 'reviewer_id', name='uq_review_ride_reviewer'),
    )