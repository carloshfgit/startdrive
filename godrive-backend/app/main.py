from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

# --- NOVOS IMPORTS ---
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from contextlib import asynccontextmanager

# Configuração do Lifespan (Substituto moderno do @app.on_event("startup"))
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup: Conecta no Redis e inicia o Cache
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="godrive-cache")
    print("✅ Sistema de Cache (Redis) inicializado com sucesso!")
    
    yield
    
    # 2. Shutdown: (Opcional) Fechar conexões se necessário
    # await redis.close()

# Inicializa a aplicação com o lifespan
app = FastAPI(
    title="GoDrive API",
    description="Backend do Marketplace de Aulas de Direção",
    version="1.0.0",
    lifespan=lifespan # <--- Injeta aqui
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def health_check():
    return {
        "project": "GoDrive",
        "status": "online",
        "version": "1.0.0",
        "message": "O container Docker está rodando perfeitamente!"
    }