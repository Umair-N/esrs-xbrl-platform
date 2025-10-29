from typing import List, Optional, Dict

from core.security import get_password_hash
from models.user import User, UserStatus
from psycopg2.extras import RealDictCursor
from schemas.user import UserCreate, UserUpdate
from datetime import datetime, timezone
from database.resilience import with_db_retry


class UserCRUD:
    def create_user(self, user: UserCreate, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(
                "SELECT id FROM users WHERE email = %(email)s OR username = %(username)s",
                {"email": user.email, "username": user.username},
            )
            if cursor.fetchone():
                return None

            hashed_password = get_password_hash(user.password)

            now_utc = datetime.now(timezone.utc)

            query = """
                INSERT INTO users (
                    email, username, hashed_password, full_name,
                    is_active, is_verified, role, company, designation,
                    status, last_login, last_accessed_at,
                    created_at, updated_at, platform_access,
                    password_changed_at, password_history, mfa_enabled, mfa_secret
                )
                VALUES (
                    %(email)s, %(username)s, %(hashed_password)s, %(full_name)s,
                    %(is_active)s, %(is_verified)s, %(role)s, %(company)s, %(designation)s,
                    %(status)s, %(last_login)s, %(last_accessed_at)s,
                    %(created_at)s, %(updated_at)s, %(platform_access)s,
                    %(password_changed_at)s, %(password_history)s, %(mfa_enabled)s, %(mfa_secret)s
                )
                RETURNING id, email, username, hashed_password, full_name,
                        is_active, is_verified, role, created_at, updated_at,
                        company, designation, status, last_login, last_accessed_at, platform_access,
                        password_changed_at, password_history, mfa_enabled, mfa_secret
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
                    "platform_access": False,
                    # NEW: Password security and MFA fields
                    "password_changed_at": now_utc,
                    "password_history": "[]",  # Empty JSON array
                    "mfa_enabled": False,
                    "mfa_secret": None,
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
    @with_db_retry(max_retries=3, delay=0.5)
    def get_user_by_email(self, email: str, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE email = %(email)s"
            cursor.execute(query, {"email": email})
            result = cursor.fetchone()
            return User(**result) if result else None
        finally:
            cursor.close()

    @with_db_retry(max_retries=3, delay=0.5)
    def get_user_by_id(self, user_id: int, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE id = %(id)s"
            cursor.execute(query, {"id": user_id})
            result = cursor.fetchone()
            return User(**result) if result else None
        finally:
            cursor.close()
    def get_all_users(
        self,
        db,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: Optional[str] = None,
        filters: Optional[Dict[str, str]] = None
    ) -> List[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            valid_columns = {
                "created_at",
                "username",
                "email",
                "full_name",
                "last_login",
                "last_accessed_at",
                "is_active",
                "is_verified",
                "role",
                "company",
                "platform_access",
                "designation",
                "status"
            }

            # Validate sort_by
            if sort_by not in valid_columns:
                sort_by = "created_at"

            # Validate sort_order
            sort_order = "DESC" if sort_order.lower() == "desc" else "ASC"

            base_query = "SELECT * FROM users"
            conditions, params = self._build_conditions(search, filters, valid_columns)

            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)

            base_query += f" ORDER BY {sort_by} {sort_order} OFFSET %(skip)s LIMIT %(limit)s"
            params["skip"] = skip
            params["limit"] = limit

            cursor.execute(base_query, params)
            rows = cursor.fetchall()

            return [User(**row) for row in rows]
        finally:
            cursor.close()

    def count_users(
        self,
        db,
        search: Optional[str] = None,
        filters: Optional[Dict[str, str]] = None
    ) -> int:
        cursor = db.cursor()
        try:
            valid_columns = {
                "created_at",
                "username",
                "email",
                "full_name",
                "last_login",
                "last_accessed_at",
                "is_active",
                "is_verified",
                "role",
                "company",
                "platform_access",
                "designation",
                "status"
            }

            base_query = "SELECT COUNT(*) FROM users"
            conditions, params = self._build_conditions(search, filters, valid_columns)

            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)

            cursor.execute(base_query, params)
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def _build_conditions(
        self,
        search: Optional[str],
        filters: Optional[Dict[str, str]],
        valid_columns: set
    ):
        """Shared helper to build WHERE conditions safely."""
        conditions = []
        params = {}

        if search:
            conditions.append("username ILIKE %(search)s")
            params["search"] = f"%{search}%"

        if filters:
            for key, value in filters.items():
                if key in valid_columns:
                    param_name = f"f_{key}"
                    conditions.append(f"{key} = %({param_name})s")
                    params[param_name] = value

        return conditions, params

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

            if user_data.last_accessed_at is not None: 
                update_fields.append("last_accessed_at = %(last_accessed_at)s")
                params["last_accessed_at"] = user_data.last_accessed_at

            if user_data.last_login is not None: 
                update_fields.append("last_login = %(last_login)s")
                params["last_login"] = user_data.last_login

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
    
    def grant_access(self, user_id: int, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE users SET platform_access = true WHERE id = %(id)s RETURNING *"
            cursor.execute(query, {"id": user_id})
            result = cursor.fetchone()
            db.commit()
            return User(**result) if result else None
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()
    def revoke_access(self, user_id: int, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE users SET platform_access = false WHERE id = %(id)s RETURNING *"
            cursor.execute(query, {"id": user_id})
            result = cursor.fetchone()
            db.commit()
            return User(**result) if result else None
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()


    def enable(self, user_id: int, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Query to get the user by user_id
            query = """
                SELECT * FROM users WHERE id = %(id)s;
            """
            cursor.execute(query, {"id": user_id})
            user = cursor.fetchone()

            if user:
                # Update user status, is_active, and platform_access
                update_query = """
                    UPDATE users
                    SET status = %(status)s, is_active = %(is_active)s, platform_access = %(platform_access)s
                    WHERE id = %(id)s
                    RETURNING *;
                """
                cursor.execute(update_query, {
                    "status": UserStatus.active.value,  # Using Enum's value as a string
                    "is_active": True,
                    "platform_access": True,  # Enable platform access
                    "id": user_id
                })
                db.commit()  # Commit the transaction

                updated_user = cursor.fetchone()  # Get the updated user
                return User(**updated_user) if updated_user else None
            
            return None  # Return None if the user wasn't found

        except Exception as error:
            db.rollback()  # Rollback in case of an error
            raise error

        finally:
            cursor.close()



    def disable(self, user_id: int, db) -> Optional[User]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            # Query to get the user by user_id
            query = """
                SELECT * FROM users WHERE id = %(id)s;
            """
            cursor.execute(query, {"id": user_id})
            user = cursor.fetchone()

            if user:
                # Update user status, is_active, and platform_access
                update_query = """
                    UPDATE users
                    SET status = %(status)s, is_active = %(is_active)s, platform_access = %(platform_access)s
                    WHERE id = %(id)s
                    RETURNING *;
                """
                cursor.execute(update_query, {
                    "status": UserStatus.disabled.value,  # Using Enum's value as a string
                    "is_active": False,
                    "platform_access": False,  # Disable platform access
                    "id": user_id
                })
                db.commit()  # Commit the transaction

                updated_user = cursor.fetchone()  # Get the updated user
                return User(**updated_user) if updated_user else None
            
            return None  # Return None if the user wasn't found

        except Exception as error:
            db.rollback()  # Rollback in case of an error
            raise error

        finally:
            cursor.close()



user_crud = UserCRUD()
