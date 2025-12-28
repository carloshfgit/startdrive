from fastapi import FastAPI
from app.api.v1.router import api_router # <--- Adicione o import
from app.core.config import settings     # <--- Adicione o import

# Inicializa a aplicação
app = FastAPI(
    title="GoDrive API",
    description="Backend do Marketplace de Aulas de Direção",
    version="1.0.0"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Rota de Health Check (Verificação de Saúde)
@app.get("/")
async def health_check():
    """
    Rota raiz para verificar se a API está online.
    """
    return {
        "project": "GoDrive",
        "status": "online",
        "version": "1.0.0",
        "message": "O container Docker está rodando perfeitamente!"
    }