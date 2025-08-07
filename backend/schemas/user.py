from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    company: Optional[str] = None
    designation: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    role: str
    company: str
    platform_access: bool
    designation: str
    status: Literal["active", "inactive", "pending", "disabled"]
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    last_accessed_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[str] = None
    company: Optional[str] = None
    platform_access: Optional[bool] = None
    designation: Optional[str] = None
    status: Optional[Literal["active", "inactive", "pending", "disabled"]] = None
    last_login: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
