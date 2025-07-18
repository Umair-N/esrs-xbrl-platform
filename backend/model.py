from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    role: str
    created_at: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str

class ReportBlock(BaseModel):
    id: str
    content: str
    type: str
    tags: List[str] = []

class ReportDocument(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    blocks: List[ReportBlock]
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None

class TextUpload(BaseModel):
    text: str
    title: Optional[str] = "Pasted Report"