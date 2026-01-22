# app/repositories/review_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.infrastructure.db.models.review import Review
from app.application.dtos import CreateReviewDTO

class ReviewRepository:
    
    def create(self, db: Session, reviewer_id: int, reviewee_id: int, review_in: CreateReviewDTO):
        db_review = Review(
            ride_id=review_in.ride_id,
            reviewer_id=reviewer_id,
            reviewee_id=reviewee_id,
            rating=review_in.rating,
            comment=review_in.comment
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    def get_by_user(self, db: Session, user_id: int, limit: int = 20):
        """Lista as avaliações que um usuário RECEBEU."""
        return db.query(Review)\
                 .filter(Review.reviewee_id == user_id)\
                 .order_by(Review.created_at.desc())\
                 .limit(limit)\
                 .all()

    def get_stats_by_user(self, db: Session, user_id: int):
        """Calcula a média e o total de avaliações recebidas."""
        result = db.query(
            func.avg(Review.rating).label("average"),
            func.count(Review.id).label("count")
        ).filter(Review.reviewee_id == user_id).first()
        
        return {
            "average": round(result.average, 1) if result.average else 0.0,
            "count": result.count
        }
    
    def get_existing_review(self, db: Session, ride_id: int, reviewer_id: int):
        """Verifica se já existe avaliação deste usuário para esta aula."""
        return db.query(Review).filter(
            Review.ride_id == ride_id,
            Review.reviewer_id == reviewer_id
        ).first()