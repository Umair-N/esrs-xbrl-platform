from datetime import datetime, timedelta

from core.config import settings
from core.security import create_access_token, create_refresh_token
from crud.auth import refresh_token_crud
from database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth import RefreshTokenRequest, Token
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth_service import auth_service
from services.user_service import user_service
from utils.validators import validate_user_input

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(user: UserCreate, db=Depends(get_db)):
    # Validate input
    validate_user_input(user.email, user.username, user.password)

    # Check if user already exists
    existing_user = user_service.get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create user
    created_user = user_service.create_user(user, db)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    return {
        "message": "User registered successfully",
        "user": {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
            "full_name": created_user.full_name,
        },
    }


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db=Depends(get_db)):
    user = auth_service.authenticate_user(
        user_credentials.email, user_credentials.password, db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    # Store refresh token
    expires_at = datetime.utcnow() + refresh_token_expires
    refresh_token_crud.store_refresh_token(user.id, refresh_token, expires_at, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: RefreshTokenRequest, db=Depends(get_db)):
    # Verify refresh token
    user_id = refresh_token_crud.verify_refresh_token(token_data.refresh_token, db)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    # Get user
    user = user_service.get_user_by_id(user_id, db)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    # Revoke old refresh token and store new one
    refresh_token_crud.revoke_refresh_token(token_data.refresh_token, db)
    expires_at = datetime.utcnow() + refresh_token_expires
    refresh_token_crud.store_refresh_token(user.id, new_refresh_token, expires_at, db)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(token_data: RefreshTokenRequest, db=Depends(get_db)):
    # Revoke refresh token
    success = refresh_token_crud.revoke_refresh_token(token_data.refresh_token, db)

    return {
        "message": "Successfully logged out" if success else "Token already invalid"
    }
