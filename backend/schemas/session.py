from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class SessionCreate(BaseModel):
    """
    Pydantic model for creating or updating an editor session.
    """
    name: str
    data: Dict[str, Any]


class SessionSummary(BaseModel):
    """
    Lightweight view of a session for listing purposes.
    """
    id: str
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EditorSessionResponse(SessionSummary):
    """
    Full session representation including the stored data.
    """
    data: Dict[str, Any]