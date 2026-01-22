"""
UserMapper

Converte entre UserEntity (domínio) e User (SQLAlchemy model).
"""
from typing import Optional

from app.domain.entities.user import UserEntity
from app.infrastructure.db.models.user import User as UserModel


class UserMapper:
    """
    Mapper para conversão bidirecional entre User Entity e Model.
    """
    
    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        """
        Converte um User SQLAlchemy model para UserEntity.
        """
        return UserEntity(
            id=model.id,
            full_name=model.full_name or "",
            email=model.email,
            user_type=model.user_type or "student",
            is_active=model.is_active if model.is_active is not None else True,
            is_superuser=model.is_superuser if model.is_superuser is not None else False,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    @staticmethod
    def to_model(entity: UserEntity, existing_model: Optional[UserModel] = None) -> UserModel:
        """
        Converte uma UserEntity para User SQLAlchemy model.
        """
        if existing_model:
            existing_model.full_name = entity.full_name
            existing_model.email = entity.email
            existing_model.user_type = entity.user_type
            existing_model.is_active = entity.is_active
            existing_model.is_superuser = entity.is_superuser
            return existing_model
        
        return UserModel(
            id=entity.id if entity.id and entity.id > 0 else None,
            full_name=entity.full_name,
            email=entity.email,
            user_type=entity.user_type,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
        )
    
    @staticmethod
    def to_entity_list(models: list[UserModel]) -> list[UserEntity]:
        """Converte lista de models para lista de entities."""
        return [UserMapper.to_entity(m) for m in models]
