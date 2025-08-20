from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "SecureVote"
    API_V1_STR: str = "/api"
    # For dev keep SQLite; can swap to Postgres later
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./securevote.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    JWT_SECRET_KEY: str = "CHANGE_THIS_IN_PROD"
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list[str] = ["*"]  # restrict in prod

    class Config:
        env_file = ".env"

settings = Settings()
