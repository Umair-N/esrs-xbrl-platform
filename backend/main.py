# File: main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional, List

# Import from your existing modules
from core.config import ALLOWED_ORIGINS , ALLOWED_EXTENSIONS ,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,DATABASE_URL, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY
from database import get_db, init_db
from model import User, UserCreate, UserLogin, Token, RefreshToken
from auth import (
    get_current_user, 
    require_role, 
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_user_by_email,
    create_user,
    store_refresh_token,
    verify_refresh_token,
    revoke_refresh_token
)

# Initialize FastAPI app
app = FastAPI(title="Authentication API with File Upload", version="1.0.0")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# API Routes
@app.post("/register", response_model=dict)
async def register(user: UserCreate, db = Depends(get_db)):
    # Check if user already exists
    existing_user = get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    created_user = create_user(user, db)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    return {
        "message": "User registered successfully",
        "user": {
            "id": created_user.id,
            "email": created_user.email,
            "username": created_user.username,
            "full_name": created_user.full_name
        }
    }

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db = Depends(get_db)):
    user = authenticate_user(user_credentials.email, user_credentials.password, db)
    
    print("user", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    
    # Store refresh token
    store_refresh_token(
    user.id, 
    refresh_token, 
    datetime.utcnow() + refresh_token_expires
    )

    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh", response_model=dict)
async def refresh_token(refresh_data: RefreshToken, db = Depends(get_db)):
    try:
        from jose import jwt, JWTError
        
        payload = jwt.decode(refresh_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify refresh token exists in database
    user_id = verify_refresh_token(refresh_data.refresh_token, db)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Get user
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@app.post("/logout")
async def logout(refresh_data: RefreshToken, db = Depends(get_db)):
    # Revoke refresh token
    revoke_refresh_token(refresh_data.refresh_token, db)
    return {"message": "Logged out successfully"}

@app.get("/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, this is a protected route!"}

@app.get("/admin-only")
async def admin_only_route(current_user: dict = Depends(require_role("admin"))):
    return {"message": f"Hello admin {current_user.username}, you have admin access!"}

@app.get("/users", response_model=List[User])
async def get_all_users(
    current_user: dict = Depends(require_role("admin")), 
    db = Depends(get_db)
):
    from database import get_all_users
    return get_all_users(db)

@app.get("/")
async def root():
    return {"message": "Authentication API with File Upload is running"}

# Include file upload routes
from routes.file_upload_routes import router as file_router
app.include_router(file_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)