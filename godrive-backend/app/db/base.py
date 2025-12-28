from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Importamos os modelos aqui para o Alembic detectá-los
from app.models.user import User