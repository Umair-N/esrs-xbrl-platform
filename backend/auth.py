from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sqlite3
from typing import Optional
from core.config import SECRET_KEY, ALGORITHM, DATABASE_URL, pwd_context
from model import UserCreate, User
from database import get_db

# HTTP Bearer token scheme
security = HTTPBearer()

class TokenData:
    def __init__(self, email: Optional[str] = None):
        self.email = email

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_id(user_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "email": user[1],
            "username": user[2],
            "hashed_password": user[3],
            "full_name": user[4],
            "is_active": user[5],
            "is_verified": user[6],
            "role": user[7],
            "created_at": user[8],
            "updated_at": user[9]
        }
    return None

def store_refresh_token(user_id: int, token: str, expires_at: datetime):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO refresh_tokens (user_id, token, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, token, expires_at))
    
    conn.commit()
    conn.close()

def verify_refresh_token(token: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT user_id FROM refresh_tokens 
        WHERE token = ? AND expires_at > datetime('now')
    """, (token,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

def revoke_refresh_token(token: str):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM refresh_tokens WHERE token = ?", (token,))
    conn.commit()
    conn.close()

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email=token_data.email, db=db)  # ✅ Pass proper db connection
    if user is None:
        raise credentials_exception

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user

# Role-based access control
def require_role(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role and current_user["role"] != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

def authenticate_user(email: str, password: str, db) -> Optional[User]:
    print("authenticate_user", email, password, db)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_row = cursor.fetchone()

    if not user_row:
        return None

    if not verify_password(password, user_row[3]):  # hashed_password is at index 3
        return None

    return User(
        id=user_row[0],
        email=user_row[1],
        username=user_row[2],
        full_name=user_row[4],
        is_active=bool(user_row[5]),
        is_verified=bool(user_row[6]),
        role=user_row[7],
        created_at=user_row[8],
    )

def create_user(user: UserCreate, db) -> User:
    """Create a new user in the database if username/email is unique."""

    cursor = db.cursor()

    # Check for existing email or username
    cursor.execute("SELECT * FROM users WHERE email = ? OR username = ?", (user.email, user.username))
    if cursor.fetchone():
        return None  # User with email or username already exists

    hashed_password = pwd_context.hash(user.password)

    cursor.execute("""
        INSERT INTO users (email, username, hashed_password, full_name, is_active, is_verified, role)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user.email,
        user.username,
        hashed_password,
        user.full_name,
        True,       # is_active
        False,      # is_verified
        "user"      # default role
    ))

    db.commit()

    user_id = cursor.lastrowid

    # Fetch full row to return
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    return User(
        id=row[0],
        email=row[1],
        username=row[2],
        full_name=row[4],
        is_active=row[5],
        is_verified=row[6],
        role=row[7],
        created_at=row[8],
    )

def get_user_by_email(email: str, db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        return {
            "id": user[0],
            "email": user[1],
            "username": user[2],
            "hashed_password": user[3],
            "full_name": user[4],
            "is_active": user[5],
            "is_verified": user[6],
            "role": user[7],
            "created_at": user[8],
            "updated_at": user[9]
        }
    return None