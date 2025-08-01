import psycopg2
from crud.user import user_crud
from database.session import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import User
from services.auth_service import auth_service

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print(f"Attempting to verify token...")  # Debug

    try:
        email = auth_service.verify_token(credentials.credentials)
        print(f"Token verification result - email: {email}")  # Debug

        if email is None:
            print("Token verification returned None")  # Debug
            raise credentials_exception
    except Exception as e:
        print(f"Token verification exception: {e}")  # Debug
        raise credentials_exception

    print(f"Querying database for user: {email}")  # Debug

    # Get user - this is where psycopg2 error might occur
    try:
        user = user_crud.get_user_by_email(email=email, db=db)
        print(f"Database query result - user found: {user is not None}")  # Debug

        if user is None:
            print("User not found in database")  # Debug
            raise credentials_exception

        print(f"User active status: {user.is_active}")  # Debug
        if not user.is_active:
            print("User is inactive")  # Debug
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
            )

        print("User authentication successful")  # Debug
        return user

    except psycopg2.Error as e:
        print(f"Database error: {e}")  # Debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
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
