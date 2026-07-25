from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediSphere AI"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    # Use SQLite by default for easy development fallback
    DATABASE_URL: str = Field(
        default="sqlite:///./medisphere.db",
        validation_alias="DATABASE_URL"
    )
    
    # JWT Auth Settings
    SECRET_KEY: str = Field(
        default="super-secret-key-change-in-production",
        validation_alias="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MinIO / S3 Storage
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "medisphere-documents"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
