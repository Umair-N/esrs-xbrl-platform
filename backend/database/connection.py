import logging
import psycopg2
from psycopg2 import pool
from core.config import settings

class DatabaseConnection:
    _initialized = False
    connection_pool = None

    def __init__(self):
        if not self._initialized:
            self.initialize_pool()
            self._initialized = True

    def initialize_pool(self):
        try:
            if settings.DATABASE_URL:
                # If DATABASE_URL is provided in the settings, use it
                self.connection_pool = pool.SimpleConnectionPool(
                    1, 10, settings.DATABASE_URL
                )
            else:
                # Fallback to individual parameters if DATABASE_URL is not provided
                db_config = {
                    "host": settings.NEON_HOST,
                    "database": settings.NEON_DATABASE,
                    "user": settings.NEON_USER,
                    "password": settings.NEON_PASSWORD,
                    "port": settings.NEON_PORT,
                    "sslmode": "require",
                }
                self.connection_pool = pool.SimpleConnectionPool(1, 10, **db_config)

            logging.info("✅ Database connection pool created successfully")
        except Exception as error:
            logging.error(f"❌ Error creating database connection pool: {error}")
            raise

    def get_connection(self):
        """Retrieve a connection from the pool."""
        try:
            connection = self.connection_pool.getconn()
            if connection.closed != 0:
                logging.error("❌ Connection is closed, retrying...")
                return None
            return connection
        except Exception as e:
            logging.error(f"❌ Error getting connection from pool: {e}")
            raise

    def return_connection(self, connection):
        """Return the connection to the pool."""
        if connection:
            self.connection_pool.putconn(connection)

    def close_all_connections(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logging.info("✅ All connections closed")

    def is_connection_alive(self):
        """Check if a connection to the database is alive."""
        connection = None
        try:
            connection = self.get_connection()
            if not connection:
                return False
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except psycopg2.OperationalError as e:
            logging.error(f"❌ OperationalError during connection check: {e}")
            return False
        except Exception as e:
            logging.error(f"❌ Unexpected error during connection check: {e}")
            return False
        finally:
            if connection:
                self.return_connection(connection)

# Singleton instance
db_manager = DatabaseConnection()
