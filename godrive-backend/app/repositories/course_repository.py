from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.course import Course, Module, Lesson, Enrollment
from app.schemas.course import CourseCreate, ModuleCreate, LessonCreate

class CourseRepository:
    
    # --- CURSOS ---

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, published_only: bool = True):
        """Lista cursos (padrão: apenas os publicados)."""
        query = db.query(Course)
        if published_only:
            query = query.filter(Course.is_published == True)
        return query.order_by(desc(Course.created_at)).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, course_id: int):
        """Busca um curso pelo ID."""
        return db.query(Course).filter(Course.id == course_id).first()

    def create(self, db: Session, course: CourseCreate):
        db_obj = Course(
            title=course.title,
            description=course.description,
            price=course.price,
            cover_image_url=course.cover_image_url,
            is_published=course.is_published
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # --- CONTEÚDO (MÓDULOS E AULAS) ---

    def create_module(self, db: Session, course_id: int, module: ModuleCreate):
        db_module = Module(
            course_id=course_id,
            title=module.title,
            order=module.order
        )
        db.add(db_module)
        db.commit()
        db.refresh(db_module)
        return db_module

    def create_lesson(self, db: Session, module_id: int, lesson: LessonCreate):
        db_lesson = Lesson(
            module_id=module_id,
            title=lesson.title,
            video_url=lesson.video_url,
            duration_seconds=lesson.duration_seconds,
            description=lesson.description,
            order=lesson.order
        )
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson

    # --- MATRÍCULAS (ALUNO) ---

    def enroll_user(self, db: Session, user_id: int, course_id: int, price_paid: float):
        """Registra a compra/matrícula de um aluno."""
        db_enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            price_paid=price_paid
        )
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment

    def get_enrollment(self, db: Session, user_id: int, course_id: int):
        """Verifica se o aluno já comprou este curso."""
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()

    def get_my_courses(self, db: Session, user_id: int):
        """Lista todos os cursos comprados por um aluno."""
        # Join para trazer os dados do curso junto com a matrícula
        return db.query(Enrollment)\
                 .join(Course)\
                 .filter(Enrollment.user_id == user_id)\
                 .order_by(desc(Enrollment.purchased_at))\
                 .all()