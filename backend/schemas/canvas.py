from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel


class CanvasCreate(BaseModel):
    """
    Schema used when persisting a new canvas state. Clients send the
    serialized report document via the ``data`` field. An optional
    ``name`` allows the frontend to supply a descriptive title (for
    example, the report's original filename). ``report_id`` can be
    provided to link this canvas back to its source report.
    """

    name: Optional[str] = None
    data: Any
    report_id: Optional[str] = None


class CanvasResponse(BaseModel):
    """
    Schema returned when a canvas state is created or fetched. The
    ``data`` field contains the deserialized report JSON and can be
    directly consumed by the frontend. Timestamps are returned as
    strings for easy display.
    """

    id: str
    name: Optional[str] = None
    data: Any
    report_id: Optional[str] = None
    # include the user_id for completeness
    user_id: Optional[int] = None
    # Use datetime types for timestamps; Pydantic will convert them to ISO strings
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """
        Enable ORM mode so that Pydantic can accept objects with attribute access.
        While we currently pass dictionaries, this setting allows for flexibility
        should we return SQLAlchemy models directly in the future.
        """
        orm_mode = True