import psycopg2
from crud.user import user_crud
from database.session import get_db
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import User
from services.auth_service import auth_service

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    request: Request,  # <-- we'll read the cookie from here
    db=Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Get access_token from cookies
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    # 2. Verify token
    try:
        email = auth_service.verify_token(token)
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # 3. Retrieve user
    try:
        user = user_crud.get_user_by_email(email=email, db=db)
        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        return user

    except psycopg2.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )
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
