import enum
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Enum, Integer
from models.base import Base  


class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"
    disabled = "disabled"

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String, default="user")
    company: Mapped[str] = mapped_column(String, default="")
    platform_access: Mapped[bool] = mapped_column(Boolean, default=False)
    designation: Mapped[str] = mapped_column(String, default="")
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="userstatus", create_type=False),  
        default=UserStatus.pending
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_accessed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Password security fields
    password_changed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True, 
        default=lambda: datetime.now(timezone.utc)
    )
    password_history: Mapped[Optional[str]] = mapped_column(String, nullable=True) 
    
    # MFA for production environment access
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String, nullable=True)
