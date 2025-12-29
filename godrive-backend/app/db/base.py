from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# NOTE: Do not import models here to avoid circular imports at app runtime.
# Alembic imports models explicitly (see migrations/env.py) when autogenerating migrations.