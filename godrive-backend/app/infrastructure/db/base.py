"""
Base SQLAlchemy

Declarative base para todos os models da aplicação.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# NOTE: Do not import models here to avoid circular imports at app runtime.
# Alembic imports models explicitly (see migrations/env.py) when autogenerating migrations.

__all__ = ["Base"]
