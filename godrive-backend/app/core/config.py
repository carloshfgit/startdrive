from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GoDrive"
    
    # --- NOVOS CAMPOS DE SEGURANÇA (O erro estava aqui) ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # --- Variáveis do Banco de Dados ---
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    DATABASE_URL: str

    # --- NOVOS CAMPOS: INTEGRAÇÃO FINANCEIRA (STRIPE) ---
    # Chave secreta para criar cobranças (começa com sk_test_...)
    STRIPE_API_KEY: str 
    # Chave para assinar o Webhook e evitar fraudes (começa com whsec_...)
    STRIPE_WEBHOOK_SECRET: str 
    
    # Taxa da Plataforma (Ex: 0.15 para 15%)
    PLATFORM_FEE_PERCENT: float = 0.15

    class Config:
        env_file = ".env"
        case_sensitive = True
        # Isso permite que existam variáveis extras no .env sem quebrar o app
        extra = "ignore" 

settings = Settings()