import os
from typing import List, Set, Optional
from functools import lru_cache

from pydantic import validator, Field
from pydantic_settings import BaseSettings
import psycopg2
from psycopg2 import pool
import logging

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

    # Neon DB (PostgreSQL) - Individual components
    NEON_HOST: str
    NEON_DATABASE: str
    NEON_USER: str
    NEON_PASSWORD: str
    NEON_PORT: int = 5432
    
    # SSL Configuration - Fixed for Neon
    PGSSLMODE: str = "require"
    PGCHANNELBINDING: str = "prefer"  # Changed from 'require' to 'prefer'
    
    # Connection Pool Settings
    DB_POOL_MIN_CONN: int = 1
    DB_POOL_MAX_CONN: int = 10
    DB_CONNECT_TIMEOUT: int = 10
    DB_COMMAND_TIMEOUT: int = 30
    
    # Database URL (constructed)
    DATABASE_URL: Optional[str] = None

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
    UPLOAD_DIRECTORY: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".doc"}
    ALLOWED_FILE_TYPES: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"]
    
    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)

    @validator("DATABASE_URL", pre=True, always=True)
    def build_database_url(cls, v, values):
        """Build DATABASE_URL from individual components if not provided"""
        if v:
            return v
        
        # Build from components
        host = values.get("NEON_HOST")
        database = values.get("NEON_DATABASE")
        user = values.get("NEON_USER")
        password = values.get("NEON_PASSWORD")
        port = values.get("NEON_PORT", 5432)
        sslmode = values.get("PGSSLMODE", "require")
        
        if all([host, database, user, password]):
            return f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
        return None

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Ensure secret key is secure in production"""
        if v == "your-secret-key-change-in-production":
            logger.warning("Using default SECRET_KEY! Change this in production!")
        return v

    class Config:
        env_file = "config.env"
        extra = "forbid"
        case_sensitive = True


class DatabaseManager:
    """Enhanced database manager with connection pooling and error handling"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._pool = None
        self._connection_params = self._get_connection_params()
    
    def _get_connection_params(self) -> dict:
        """Get psycopg2 connection parameters"""
        return {
            'host': self.settings.NEON_HOST,
            'database': self.settings.NEON_DATABASE,
            'user': self.settings.NEON_USER,
            'password': self.settings.NEON_PASSWORD,
            'port': self.settings.NEON_PORT,
            'sslmode': self.settings.PGSSLMODE,
            'connect_timeout': self.settings.DB_CONNECT_TIMEOUT,
            'options': f'-c statement_timeout={self.settings.DB_COMMAND_TIMEOUT * 1000}',  # milliseconds
        }
    
    def create_pool(self):
        """Create connection pool with error handling"""
        try:
            self._pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.settings.DB_POOL_MIN_CONN,
                maxconn=self.settings.DB_POOL_MAX_CONN,
                **self._connection_params
            )
            logger.info("Database connection pool created successfully")
            return self._pool
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get connection from pool with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self._pool:
                    self.create_pool()
                
                conn = self._pool.getconn()
                
                # Test connection
                with conn.cursor() as cur:
                    cur.execute('SELECT 1')
                
                return conn
                
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                
                # Reset pool on connection failure
                if self._pool:
                    try:
                        self._pool.closeall()
                    except:
                        pass
                    self._pool = None
    
    def return_connection(self, conn):
        """Return connection to pool"""
        if self._pool and conn:
            self._pool.putconn(conn)
    
    def close_pool(self):
        """Close all connections in pool"""
        if self._pool:
            self._pool.closeall()
            self._pool = None
            logger.info("Database connection pool closed")


# Context manager for database operations
class DatabaseConnection:
    """Context manager for database connections"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.conn = None
    
    def __enter__(self):
        self.conn = self.db_manager.get_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                try:
                    self.conn.rollback()
                except:
                    pass
            else:
                try:
                    self.conn.commit()
                except:
                    pass
            
            self.db_manager.return_connection(self.conn)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Initialize settings and database manager
settings = get_settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

# Initialize database manager
db_manager = DatabaseManager(settings)

# Usage examples:
def example_database_usage():
    """Example of how to use the database connection"""
    
    # Method 1: Using context manager (recommended)
    with DatabaseConnection(db_manager) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM your_table LIMIT 1")
            result = cur.fetchall()
            return result
    
    # Method 2: Manual connection handling
    conn = None
    try:
        conn = db_manager.get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM your_table LIMIT 1")
            result = cur.fetchall()
            conn.commit()
            return result
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            db_manager.return_connection(conn)


# Environment-specific configuration
def configure_logging():
    """Configure logging based on environment"""
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

configure_logging()