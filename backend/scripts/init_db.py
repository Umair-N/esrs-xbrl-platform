import logging

import psycopg2
from core.config import settings
from core.security import get_password_hash


def create_admin_user():
    """Create initial admin user"""
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

        # Check if admin user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", ("admin@example.com",))
        if cursor.fetchone():
            print("Admin user already exists")
            return

        # Create admin user
        admin_password = "admin123"  # Change this in production
        hashed_password = get_password_hash(admin_password)

        cursor.execute(
            """
            INSERT INTO users (email, username, hashed_password, full_name, is_active, is_verified, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                "admin@example.com",
                "admin",
                hashed_password,
                "System Administrator",
                True,
                True,
                "admin",
            ),
        )

        connection.commit()

        logging.info("Admin user created successfully")
        print("Admin user created successfully")
        print("Email: admin@example.com")
        print("Password: admin123")
        print("⚠️  Please change the admin password after first login!")

    except Exception as error:
        logging.error(f"Error creating admin user: {error}")
        print(f"Error creating admin user: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_admin_user()
