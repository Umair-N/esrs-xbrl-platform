import logging

import psycopg2
from core.config import settings


def create_tables():
    """Create database tables"""
    try:
        # Connect to database
        if settings.DATABASE_URL:
            connection = psycopg2.connect(settings.DATABASE_URL)
        else:
            connection = psycopg2.connect(
                host=settings.NEON_HOST,
                database=settings.NEON_DATABASE,
                user=settings.NEON_USER,
                password=settings.NEON_PASSWORD,
                port=settings.NEON_PORT,
                sslmode="require",
            )

        cursor = connection.cursor()

        # Read and execute SQL file
        with open("migrations/create_tables.sql", "r") as file:
            sql_script = file.read()

        cursor.execute(sql_script)
        connection.commit()

        logging.info("Database tables created successfully")
        print("Database tables created successfully")

    except Exception as error:
        logging.error(f"Error creating database tables: {error}")
        print(f"Error creating database tables: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_tables()
