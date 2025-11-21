from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    """
    Pydantic model for creating or updating an editor session.
    Accepts any fields in the data dictionary to be flexible with different payload structures.
    """
    model_config = ConfigDict(extra='allow')

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