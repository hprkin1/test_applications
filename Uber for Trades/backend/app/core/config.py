from pydantic import BaseModel
import os


class Settings(BaseModel):
	environment: str = os.getenv("ENV", "dev")
	database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/swifttrade")
	jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
	jwt_algorithm: str = os.getenv("JWT_ALG", "HS256")


settings = Settings()

