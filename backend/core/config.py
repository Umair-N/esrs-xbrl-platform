"""
Extended Settings configuration for FastAPI application.  In addition to
standard application and database configuration, this settings class
detects whether the application is running on Google Cloud Platform (GCP)
via environment variables such as ``GOOGLE_CLOUD_PROJECT`` and ``GAE_ENV``.
This allows other components (e.g. file storage services) to adjust
behaviour for production versus local development.  It also exposes a
convenience property to determine if the environment is production.
"""

import os
import logging
from typing import List, Set, Optional
from functools import lru_cache

from pydantic import validator, Field
from pydantic_settings import BaseSettings
import psycopg2
from psycopg2 import pool

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Project & API Info
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "XBRL Backend"

    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database connection pieces (Supabase enabled, Neon disabled)
    # NEON Database Configuration - Disabled
    # NEON_HOST: str
    # NEON_DATABASE: str
    # NEON_USER: str
    # NEON_PASSWORD: str
    # NEON_PORT: int = 5432

    # Supabase Database Configuration (Enabled)
    SUPABASE_HOST: str = "db.iuoikdmkqmzggspcmggr.supabase.co"  # Supabase host
    SUPABASE_DATABASE: str = "postgres"  # Default Supabase database name
    SUPABASE_USER: str
    SUPABASE_PASSWORD: str
    SUPABASE_PORT: int = 5432  # Default PostgreSQL port

    # SSL Configuration (Supabase requires SSL)
    PGSSLMODE: str = "require"
    PGCHANNELBINDING: str = "prefer"  # Changed from 'require' to 'prefer'

    # Connection Pool Settings
    DB_POOL_MIN_CONN: int = 1
    DB_POOL_MAX_CONN: int = 10
    DB_CONNECT_TIMEOUT: int = 10
    DB_COMMAND_TIMEOUT: int = 30

    # Database URL (constructed for Supabase, Neon disabled)
    DATABASE_URL: Optional[str] = None

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "https://esrs-xbrl-platform.vercel.app",
        "https://briskbold.vercel.app",
        "https://xbrl.briskbold.ai",
        "https://frontend-build-171009084156.asia-east1.run.app"
        "https://frontend-pentest-171009084156.asia-east1.run.app"
    ]

    # File Upload
    UPLOAD_DIRECTORY: str = "uploads"
    MAX_FILE_SIZE: int = 70 * 1024 * 1024  # 70MB
    ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".doc"}
    ALLOWED_FILE_TYPES: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"]

    # Taxonomy storage backend configuration
    STORAGE_BACKEND: str = Field(
        default="local",
        description="Storage backend for taxonomies: 'local' or 'gcs'. If 'gcs', uploaded files are stored in a Google Cloud Storage bucket."
    )
    GCS_BUCKET: Optional[str] = Field(
        default=None,
        description="Name of the GCS bucket used when STORAGE_BACKEND is 'gcs'.",
    )
    GCS_PREFIX: Optional[str] = Field(
        default="",
        description="Optional prefix within the GCS bucket for storing taxonomy files (e.g. 'taxonomies/').",
    )

    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)

    # GCP environment variables for deployment detection
    GOOGLE_CLOUD_PROJECT: Optional[str] = Field(default=None, description="GCP Project ID for deployment detection")
    GAE_ENV: Optional[str] = Field(default=None, description="App Engine environment")

    @property
    def is_gcp_deployment(self) -> bool:
        """
        Detect if the application is running on Google Cloud Platform. Returns
        True if environment variables indicate App Engine standard environment
        or a GCP project ID is present.
        """
        return (
            (self.GAE_ENV and self.GAE_ENV.startswith("standard"))
            or (self.GOOGLE_CLOUD_PROJECT is not None)
            or (os.getenv("GAE_ENV", "").startswith("standard"))
            or (os.getenv("GOOGLE_CLOUD_PROJECT") is not None)
        )

    @property
    def is_production(self) -> bool:
        """Check if running in a production environment."""
        return self.ENVIRONMENT.lower() == "production"

    @validator("DATABASE_URL", pre=True, always=True)
    def build_database_url(cls, v, values):
        """Construct DATABASE_URL from individual components if not provided."""
        if v:
            return v
        # Checking for Supabase configuration (Neon is disabled)
        host = values.get("SUPABASE_HOST")
        database = values.get("SUPABASE_DATABASE")
        user = values.get("SUPABASE_USER")
        password = values.get("SUPABASE_PASSWORD")
        port = values.get("SUPABASE_PORT", 5432)
        sslmode = values.get("PGSSLMODE", "require")
        channel_binding = values.get("PGCHANNELBINDING", "prefer")

        if all([host, database, user, password]):
            return f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode={sslmode}&channel_binding={channel_binding}"
        return None

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Warn if the secret key is left at its default."""
        if v == "your-secret-key-change-in-production":
            logger.warning("Using default SECRET_KEY! Change this in production!")
        return v

    class Config:
        env_file = "config.env"
        extra = "forbid"
        case_sensitive = True



# class DatabaseManager:
#     """Database manager with connection pooling and retry logic."""

#     def __init__(self, settings: Settings):
#         self.settings = settings
#         self._pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None
#         self._connection_params = self._get_connection_params()

#     def _get_connection_params(self) -> dict:
#         return {
#             "host": self.settings.NEON_HOST,
#             "database": self.settings.NEON_DATABASE,
#             "user": self.settings.NEON_USER,
#             "password": self.settings.NEON_PASSWORD,
#             "port": self.settings.NEON_PORT,
#             "sslmode": self.settings.PGSSLMODE,
#             "connect_timeout": self.settings.DB_CONNECT_TIMEOUT,
#             "options": f"-c statement_timeout={self.settings.DB_COMMAND_TIMEOUT * 1000}",
#         }

#     def create_pool(self):
#         try:
#             self._pool = psycopg2.pool.ThreadedConnectionPool(
#                 minconn=self.settings.DB_POOL_MIN_CONN,
#                 maxconn=self.settings.DB_POOL_MAX_CONN,
#                 **self._connection_params,
#             )
#             logger.info("Database connection pool created successfully")
#             return self._pool
#         except Exception as e:
#             logger.error(f"Failed to create connection pool: {e}")
#             raise

#     def get_connection(self):
#         max_retries = 3
#         for attempt in range(max_retries):
#             try:
#                 if not self._pool:
#                     self.create_pool()
#                 conn = self._pool.getconn()
#                 # Test connection
#                 with conn.cursor() as cur:
#                     cur.execute("SELECT 1")
#                 return conn
#             except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
#                 logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
#                 if attempt == max_retries - 1:
#                     raise
#                 # Reset pool on failure
#                 if self._pool:
#                     try:
#                         self._pool.closeall()
#                     except Exception:
#                         pass
#                     self._pool = None

#     def return_connection(self, conn):
#         if self._pool and conn:
#             self._pool.putconn(conn)

#     def close_pool(self):
#         if self._pool:
#             self._pool.closeall()
#             self._pool = None
#             logger.info("Database connection pool closed")


# class DatabaseConnection:
#     """Context manager for database connections."""

#     def __init__(self, db_manager: DatabaseManager):
#         self.db_manager = db_manager
#         self.conn: Optional[psycopg2.extensions.connection] = None

#     def __enter__(self):
#         self.conn = self.db_manager.get_connection()
#         return self.conn

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.conn:
#             if exc_type:
#                 try:
#                     self.conn.rollback()
#                 except Exception:
#                     pass
#             else:
#                 try:
#                     self.conn.commit()
#                 except Exception:
#                     pass
#             self.db_manager.return_connection(self.conn)

class DatabaseManager:
    """Database manager with connection pooling and retry logic."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None
        self._connection_params = self._get_connection_params()

    def _get_connection_params(self) -> dict:
        return {
            "host": self.settings.SUPABASE_HOST,  # Supabase host
            "database": self.settings.SUPABASE_DATABASE,  # Supabase database
            "user": self.settings.SUPABASE_USER,  # Supabase user
            "password": self.settings.SUPABASE_PASSWORD,  # Supabase password
            "port": self.settings.SUPABASE_PORT,  # Supabase port (default is 5432)
            "sslmode": self.settings.PGSSLMODE,  # SSL mode for Supabase
            "connect_timeout": self.settings.DB_CONNECT_TIMEOUT,  # Connection timeout
            "options": f"-c statement_timeout={self.settings.DB_COMMAND_TIMEOUT * 1000}",  # Command timeout
        }

    def create_pool(self):
        try:
            self._pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.settings.DB_POOL_MIN_CONN,
                maxconn=self.settings.DB_POOL_MAX_CONN,
                **self._connection_params,
            )
            logger.info("Database connection pool created successfully")
            return self._pool
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise

    def get_connection(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self._pool:
                    self.create_pool()
                conn = self._pool.getconn()
                # Test connection
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return conn
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                # Reset pool on failure
                if self._pool:
                    try:
                        self._pool.closeall()
                    except Exception:
                        pass
                    self._pool = None

    def return_connection(self, conn):
        if self._pool and conn:
            self._pool.putconn(conn)

    def close_pool(self):
        if self._pool:
            self._pool.closeall()
            self._pool = None
            logger.info("Database connection pool closed")


class DatabaseConnection:
    """Context manager for database connections."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.conn: Optional[psycopg2.extensions.connection] = None

    def __enter__(self):
        self.conn = self.db_manager.get_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                try:
                    self.conn.rollback()
                except Exception:
                    pass
            else:
                try:
                    self.conn.commit()
                except Exception:
                    pass
            self.db_manager.return_connection(self.conn)
@lru_cache()
def get_settings() -> Settings:
    """Get a cached settings instance."""
    return Settings()


settings = get_settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

# Initialize database manager
db_manager = DatabaseManager(settings)


def configure_logging():
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


configure_logging()
