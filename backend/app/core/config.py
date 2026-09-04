from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskWeave"
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    REDIS_URL: str
    GEMINI_API_KEY: str | None = None

    class Config:
        case_sensitive = True
        extra = "ignore"
        env_file = ("../.env", ".env")

settings = Settings()
