from datetime import datetime, timedelta

from core.config import settings
from core.security import (create_access_token, create_refresh_token,
                           verify_token)
from database.session import get_db
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from schemas.auth import RefreshTokenRequest, Token
from schemas.user import UserCreate, UserLogin
from services.auth_service import auth_service
from services.user_service import user_service
from utils.validators import validate_user_input

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(user: UserCreate, db=Depends(get_db)):
    validate_user_input(user.email, user.username, user.password)

    if user_service.get_user_by_email(user.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = user_service.create_user(user, db)
    if not created_user:
        raise HTTPException(
            status_code=409, detail="Username already exists"
        )  # Changed to 409 Conflict

    return {
        "message": "User registered successfully",
        "user": {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
            "full_name": created_user.full_name,
        },
    }


@router.post("/login")  # Removed response_model=Token
async def login(user_credentials: UserLogin, db=Depends(get_db)):
    user = auth_service.authenticate_user(
        user_credentials.email, user_credentials.password, db
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Added expires_in
        }
    )

    # Set secure=True in production, False for development
    is_production = (
        getattr(settings, "ENVIRONMENT", "development").lower() == "production"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=is_production,  # Dynamic based on environment
        max_age=int(refresh_token_expires.total_seconds()),
        path="/",  # Explicitly set path
    )
    return response


@router.post("/refresh")  # Removed response_model=Token
async def refresh_token(refresh_token: str = Cookie(None), db=Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Verify user still exists and is active
    user = user_service.get_user_by_email(email, db)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )

    # Optional: Rotate refresh token for better security
    new_refresh_token = create_refresh_token(
        data={"sub": email}, expires_delta=refresh_token_expires
    )

    response = JSONResponse(
        content={
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
    )

    # Set the new refresh token
    is_production = (
        getattr(settings, "ENVIRONMENT", "development").lower() == "production"
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="strict",
        secure=is_production,
        max_age=int(refresh_token_expires.total_seconds()),
        path="/",
    )

    return response


@router.post("/logout", response_model=dict)
async def logout():
    response = JSONResponse(content={"message": "Logged out successfully"})

    # Match cookie deletion parameters with set_cookie parameters
    response.delete_cookie(key="refresh_token", path="/", samesite="strict")
    return response
