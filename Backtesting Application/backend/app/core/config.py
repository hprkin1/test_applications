from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "quantflow")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "quantflow")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "quantflow")
    SQLALCHEMY_DATABASE_URI: str | None = None

    # Redis / Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

    # File storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    STRATEGY_DIR: str = os.getenv("STRATEGY_DIR", "/app/strategies")
    DATASET_DIR: str = os.getenv("DATASET_DIR", "/app/datasets")
    RESULTS_DIR: str = os.getenv("RESULTS_DIR", "/app/results")

    # CORS
    CORS_ALLOW_ORIGINS: List[str] | str = "*"

    @field_validator("CORS_ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False

    def build_db_uri(self) -> str:
        return (
            self.SQLALCHEMY_DATABASE_URI
            or f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}"
        )

settings = Settings()
