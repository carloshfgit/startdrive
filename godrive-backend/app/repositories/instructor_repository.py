from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.instructor import InstructorProfile, InstructorStatus # <--- Importe o Enum
from app.models.user import User
from app.schemas.instructor import InstructorCreate
from geoalchemy2.elements import WKTElement

class InstructorRepository:
    
    def create(self, db: Session, user_id: int, profile: InstructorCreate):
        # Cria o ponto geográfico a partir da lat/long
        # ST_GeomFromEWKT('SRID=4326;POINT(lon lat)')
        point = f'SRID=4326;POINT({profile.longitude} {profile.latitude})'
        
        db_profile = InstructorProfile(
            id=user_id, # Mesmo ID do usuário (1:1)
            bio=profile.bio,
            hourly_rate=profile.hourly_rate,
            cnh_category=profile.cnh_category,
            vehicle_model=profile.vehicle_model,
            location=point
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    def get_by_radius(self, db: Session, lat: float, long: float, radius_km: float):
        """
        Busca instrutores dentro de um raio de X km.
        Retorna também a distância calculada.
        """
        # Ponto de referência (Aluno)
        ref_point = func.ST_SetSRID(func.ST_MakePoint(long, lat), 4326)
        
        # Filtro Geoespacial:
        # Usamos cast para Geography para calcular em METROS
        # radius_km * 1000 = metros
        query = db.query(
            InstructorProfile,
            # Calcula a distância em km para exibir no front
            (func.ST_Distance(
                InstructorProfile.location.cast(func.geography()), 
                ref_point.cast(func.geography())
            ) / 1000).label("distance")
        ).join(User).filter(
            func.ST_DWithin(
                InstructorProfile.location.cast(func.geography()),
                ref_point.cast(func.geography()),
                radius_km * 1000 # Metros
            )
        ).order_by("distance") # Ordena do mais próximo para o mais longe
        
        results = query.all()
        
        # Monta a resposta combinando dados do User + Profile + Distance
        response = []
        for profile, distance in results:
            resp = {
                "id": profile.user.id,
                "full_name": profile.user.full_name,
                "bio": profile.bio,
                "hourly_rate": profile.hourly_rate,
                "cnh_category": profile.cnh_category,
                "vehicle_model": profile.vehicle_model,
                "distance": round(distance, 2) # Arredonda para 2 casas decimais
            }
            response.append(resp)
            
        return response
    
    # --- NOVOS MÉTODOS PARA ADMIN ---
    
    def get_pending(self, db: Session):
        return db.query(InstructorProfile).filter(InstructorProfile.status == InstructorStatus.PENDING).all()

    def update_status(self, db: Session, instructor_id: int, new_status: InstructorStatus):
        profile = db.query(InstructorProfile).filter(InstructorProfile.id == instructor_id).first()
        if profile:
            profile.status = new_status
            db.commit()
            db.refresh(profile)
        return profile
    
    def update_documents(self, db: Session, instructor_id: int, cnh_url: str, vehicle_doc_url: str):
        profile = db.query(InstructorProfile).filter(InstructorProfile.id == instructor_id).first()
        if profile:
            if cnh_url: profile.cnh_url = cnh_url
            if vehicle_doc_url: profile.vehicle_doc_url = vehicle_doc_url
            db.commit()
            db.refresh(profile)
        return profile