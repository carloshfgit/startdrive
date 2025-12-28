from fastapi import FastAPI

# Inicializa a aplicação
app = FastAPI(
    title="GoDrive API",
    description="Backend do Marketplace de Aulas de Direção",
    version="1.0.0"
)

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