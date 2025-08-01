from datetime import datetime, timedelta
from typing import Optional

from core.config import settings
from core.security import get_password_hash, verify_password
from crud.auth import refresh_token_crud
from crud.user import user_crud
from fastapi import HTTPException, status
from jose import JWTError, jwt
from models.user import User


class AuthService:
    def authenticate_user(self, email: str, password: str, db) -> Optional[User]:
        user = user_crud.get_user_by_email(email, db)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None


auth_service = AuthService()
