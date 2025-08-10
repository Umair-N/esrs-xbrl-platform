import os
from typing import List, Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project & API Info
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "XBRL Backend "

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str = ""

    # Neon DB (PostgreSQL)
    NEON_HOST: str
    NEON_DATABASE: str
    NEON_USER: str
    NEON_PASSWORD: str
    NEON_PORT: int = 5432
    PGSSLMODE: str = "require"
    PGCHANNELBINDING: str = "require"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "https://esrs-xbrl-platform.vercel.app",
        "https://briskbold.vercel.app",
        "https://xbrl.briskbold.ai",
    ]

    # File Upload
    UPLOAD_DIRECTORY: str = "uploads"  # ✅ Rename here
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".doc"}
    ALLOWED_FILE_TYPES: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"]

    class Config:
        env_file = "config.env"  # ✅ Make sure your env file is named correctly
        extra = "forbid"  # recommended to catch typos


# Ensure upload directory exists
os.makedirs(Settings().UPLOAD_DIRECTORY, exist_ok=True)

# Instantiate settings
settings = Settings()
