from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.base import BaseModel


@dataclass
class User(BaseModel):
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    role: str = "user"
