from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.base import BaseModel


@dataclass
class RefreshToken(BaseModel):
    user_id: int = 0
    token: str = ""
    expires_at: Optional[datetime] = None
    is_revoked: bool = False
