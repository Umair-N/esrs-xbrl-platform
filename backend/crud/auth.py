from datetime import datetime
from typing import Optional

from models.auth import RefreshToken
from psycopg2.extras import RealDictCursor


class RefreshTokenCRUD:
    def store_refresh_token(
        self, user_id: int, token: str, expires_at: datetime, db
    ) -> Optional[RefreshToken]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
                INSERT INTO refresh_tokens (user_id, token, expires_at)
                VALUES (%(user_id)s, %(token)s, %(expires_at)s)
                RETURNING id, user_id, token, expires_at, created_at, is_revoked
            """
            cursor.execute(
                query, {"user_id": user_id, "token": token, "expires_at": expires_at}
            )
            result = cursor.fetchone()
            db.commit()
            return RefreshToken(**result) if result else None
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()

    def verify_refresh_token(self, token: str, db) -> Optional[int]:
        cursor = db.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
                SELECT user_id FROM refresh_tokens 
                WHERE token = %(token)s 
                AND expires_at > NOW() 
                AND is_revoked = false
            """
            cursor.execute(query, {"token": token})
            result = cursor.fetchone()
            return result["user_id"] if result else None
        finally:
            cursor.close()

    def revoke_refresh_token(self, token: str, db) -> bool:
        cursor = db.cursor()
        try:
            query = (
                "UPDATE refresh_tokens SET is_revoked = true WHERE token = %(token)s"
            )
            cursor.execute(query, {"token": token})
            db.commit()
            return cursor.rowcount > 0
        except Exception as error:
            db.rollback()
            raise error
        finally:
            cursor.close()


refresh_token_crud = RefreshTokenCRUD()
