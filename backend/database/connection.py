import logging

import psycopg2
from core.config import settings
from psycopg2 import pool


class DatabaseConnection:
    def __init__(self):
        self.connection_pool = None
        self.initialize_pool()

    def initialize_pool(self):
        try:
            if settings.DATABASE_URL:
                self.connection_pool = pool.SimpleConnectionPool(
                    1, 10, settings.DATABASE_URL
                )
            else:
                db_config = {
                    "host": settings.NEON_HOST,
                    "database": settings.NEON_DATABASE,
                    "user": settings.NEON_USER,
                    "password": settings.NEON_PASSWORD,
                    "port": settings.NEON_PORT,
                    "sslmode": "require",
                }
                self.connection_pool = pool.SimpleConnectionPool(1, 10, **db_config)

            logging.info("✅ Neon DB connection pool created successfully")
        except Exception as error:
            logging.error(f"❌ Error creating Neon DB connection pool: {error}")
            raise

    def get_connection(self):
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        if self.connection_pool:
            self.connection_pool.closeall()

    def is_connection_alive(self):
        connection = None
        try:
            connection = self.get_connection()
            if connection.closed != 0:
                return False
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except Exception as error:
            logging.error(f"❌ Database connection check failed: {error}")
            return False
        finally:
            if connection:
                self.return_connection(connection)


# Singleton instance
db_manager = DatabaseConnection()
