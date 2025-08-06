from typing import List, Optional

from core.security import get_password_hash
from models.user import User
from psycopg2.extras import RealDictCursor
from schemas.user import UserCreate, UserUpdate
from datetime import datetime, timezone


class UserCRUD:
    def create_user(self, user: UserCreate, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Check for existing email or username
            cursor.execute(
                "SELECT id FROM users WHERE email = %(email)s OR username = %(username)s",
                {"email": user.email, "username": user.username},
            )
            if cursor.fetchone():
                return None

            # Hash password
            hashed_password = get_password_hash(user.password)

            # Get current UTC time
            now_utc = datetime.now(timezone.utc)

            # Insert new user
            query = """
                INSERT INTO users (
                    email, username, hashed_password, full_name,
                    is_active, is_verified, role, company, designation,
                    status, last_login, last_accessed_at,
                    created_at, updated_at, platform_access
                )
                VALUES (
                    %(email)s, %(username)s, %(hashed_password)s, %(full_name)s,
                    %(is_active)s, %(is_verified)s, %(role)s, %(company)s, %(designation)s,
                    %(status)s, %(last_login)s, %(last_accessed_at)s,
                    %(created_at)s, %(updated_at)s, %(platform_access)s
                )
                RETURNING id, email, username, hashed_password, full_name,
                        is_active, is_verified, role, created_at, updated_at,
                        company, designation, status, last_login, last_accessed_at, platform_access
            """
            cursor.execute(
                query,
                {
                    "email": user.email,
                    "username": user.username,
                    "hashed_password": hashed_password,
                    "full_name": user.full_name,
                    "is_active": True,
                    "is_verified": False,
                    "role": "user",
                    "company": user.company,
                    "designation": user.designation,
                    "status": "pending",
                    "last_login": now_utc,
                    "last_accessed_at": now_utc,
                    "created_at": now_utc,
                    "updated_at": now_utc,
                    "platform_access": False,  # or user.platform_access if included in schema
                },
            )

            result = cursor.fetchone()
            db.commit()
            return User(**result) if result else None

        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()
    def get_user_by_email(self, email: str, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE email = %(email)s"
            cursor.execute(query, {"email": email})
            result = cursor.fetchone()
            return User(**result) if result else None
        finally:
            cursor.close()

    def get_user_by_id(self, user_id: int, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE id = %(id)s"
            cursor.execute(query, {"id": user_id})
            result = cursor.fetchone()
            return User(**result) if result else None
        finally:
            cursor.close()

    def get_all_users(self, db) -> List[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users ORDER BY created_at DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            return [User(**row) for row in results]
        finally:
            cursor.close()

    def update_user(self, user_id: int, user_data: UserUpdate, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Build dynamic update query
            update_fields = []
            params = {"id": user_id}

            if user_data.full_name is not None:
                update_fields.append("full_name = %(full_name)s")
                params["full_name"] = user_data.full_name

            if user_data.is_active is not None:
                update_fields.append("is_active = %(is_active)s")
                params["is_active"] = user_data.is_active

            if user_data.is_verified is not None:
                update_fields.append("is_verified = %(is_verified)s")
                params["is_verified"] = user_data.is_verified

            if user_data.role is not None:
                update_fields.append("role = %(role)s")
                params["role"] = user_data.role

            if not update_fields:
                return self.get_user_by_id(user_id, db)

            update_fields.append("updated_at = CURRENT_TIMESTAMP")

            # trunk-ignore(bandit/B608)
            query = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE id = %(id)s
                RETURNING *
            """

            cursor.execute(query, params)
            result = cursor.fetchone()
            db.commit()
            return User(**result) if result else None

        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()


user_crud = UserCRUD()
