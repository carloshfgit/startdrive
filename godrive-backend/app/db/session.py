from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Cria o motor de conexão usando a URL do .env
# pool_pre_ping=True ajuda a evitar desconexões silenciosas
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria a fábrica de sessões (cada requisição usará uma dessas)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)