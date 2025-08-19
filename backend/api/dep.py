# import psycopg2
from crud.user import user_crud
from database.session import get_db
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import User
from services.auth_service import auth_service
# from jose import JWTError, ExpiredSignatureError
from datetime import timedelta
from core.config import settings
from services.user_service import user_service
from core.security import (create_access_token, create_refresh_token)

# HTTP Bearer token scheme
security = HTTPBearer()



async def get_current_user(
    request: Request,
    db=Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token and not refresh_token:
        raise credentials_exception

    # 1) Try access token first
    email = auth_service.verify_token(access_token) if access_token else None

    # 2) If access token is missing/invalid/expired, try refresh
    if not email:
        refresh_email = auth_service.verify_token(refresh_token) if refresh_token else None
        if not refresh_email:
            raise credentials_exception

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        new_access_token = create_access_token(
            data={"sub": refresh_email},
            expires_delta=access_token_expires,
        )
        new_refresh_token = create_refresh_token(
            data={"sub": refresh_email},
            expires_delta=refresh_token_expires,
        )

        # Let your middleware set the cookies
        request.state.new_tokens = {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }

        email = refresh_email

    # 3) Load user
    user = user_service.get_user_by_email(email=email, db=db)
    if not user or not user.is_active:
        raise credentials_exception

    return user

def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current_user

    return role_checker


# Convenience dependencies
def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


def require_admin(current_user: User = Depends(require_role("admin"))):
    return current_user


def require_verified_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email verification required"
        )
    return current_user
