from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with validation."""

    DATABASE_URL: str = "sqlite:///./data/clg_vermoegensschutz.db"
    JWT_SECRET: str = "change-me-in-production"
    SECRET_KEY: str = "change-me-in-production"
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""

     # JWT configuration
    JWT_EXPIRATION_MINUTES: int = 15
    JWT_REFRESH_DAYS: int = 7

      # CORS settings (DACH focus)
    ALLOWED_ORIGINS: str = "https://clg-protect.de,https://www.clg-protect.de"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
