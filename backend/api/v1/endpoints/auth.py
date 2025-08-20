from datetime import timedelta

from core.config import settings
from core.security import (create_access_token, create_refresh_token,
                           verify_token)
from database.session import get_db
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.user import UserCreate, UserLogin
from services.auth_service import auth_service
from services.user_service import user_service
from utils.validators import validate_user_input
from datetime import datetime, timezone
from schemas.user import UserUpdate
import uuid


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


@router.post("/login")  
async def login(user_credentials: UserLogin, db=Depends(get_db)):

    now_utc = datetime.now(timezone.utc)
    user = auth_service.authenticate_user(
        user_credentials.email, user_credentials.password, db
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    

    user_service.update_user(user_id=user.id, user_data=UserUpdate(last_accessed_at=now_utc, last_login=now_utc), db=db)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )


    is_production = (
        getattr(settings, "ENVIRONMENT", "development").lower() == "production"
    )

    if is_production:
        same_site, secure_flag = "none", True
    else:
        same_site, secure_flag = "lax", False


    response = JSONResponse(
        content={
            "message": "Login successful",
            # "access_token": access_token,
            # "token_type": "bearer",
            # "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite=same_site,
        secure=secure_flag, 
        max_age=int(refresh_token_expires.total_seconds()),
        path="/",  
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite=same_site,
        secure=secure_flag,
        max_age=int(access_token_expires.total_seconds()),
        path="/",  
    )

    return response


@router.post("/refresh")
async def refresh_tokens(
    rt_cookie: str = Cookie(None, alias="refresh_token"),
    db = Depends(get_db),
):
    if not rt_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = verify_token(rt_cookie, token_type="refresh")
    except Exception:
        # map any verification failure to 401 without leaking details
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    if not payload or payload.get("typ") != "refresh":
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

    new_jti = str(uuid.uuid4())
    new_access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        data={"sub": email, "jti": new_jti}, expires_delta=refresh_token_expires
    )

    response = JSONResponse(
        content={
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
    )

    is_production = (getattr(settings, "ENVIRONMENT", "development").lower() == "production")

    if is_production:
        same_site, secure_flag = "none", True
    else:
        same_site, secure_flag = "lax", False
    
    response.set_cookie(
    key="access_token",
    value=new_access_token,
    httponly=True,
    samesite=same_site,      # "lax" in dev proxy / "none" in prod HTTPS
    secure=secure_flag,      # False in dev HTTP / True in prod HTTPS
    max_age=int(access_token_expires.total_seconds()),
    path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite=same_site,
        secure=secure_flag,         
        max_age=int(refresh_token_expires.total_seconds()),
        path="/",
    )

    return response



@router.post("/logout", response_model=dict)
async def logout():
    response = JSONResponse(content={"message": "Logged out successfully"})
    is_production = (getattr(settings, "ENVIRONMENT", "development").lower() == "production")

    if is_production:
        same_site, secure_flag = "none", True
    else:
        same_site, secure_flag = "lax", False

    # Match cookie deletion parameters with set_cookie parameters
    response.delete_cookie(key="refresh_token", path="/", samesite= same_site, secure=secure_flag)
    response.delete_cookie(key="access_token", path="/", samesite= same_site, secure=secure_flag)
    return response
