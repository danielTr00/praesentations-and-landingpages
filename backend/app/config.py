import os
from pydantic_settings import BaseSettings


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

    # CORS settings - include SSLIP domain for testing
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "https://clg-protect.de,"
        "http://localhost:8000,"
        "http://127.0.0.1:8000,"
        "https://192.168.178.87.sslip.io"
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
