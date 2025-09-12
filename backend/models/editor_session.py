import uuid
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from models.base import Base
import sqlalchemy as sa
import datetime


class EditorSession(Base):
    """
    Represents an editing session for a user. This stores the editor's
    current document (as JSON) along with a user supplied name. Sessions
    are tied to individual users so that multiple users can maintain their
    own sets of documents.
    """

    __tablename__ = "editor_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Persist the full report/session JSON as a text field. Using Text instead
    # of JSON here avoids strict database dependencies while still allowing
    # arbitrary document structures to be stored.
    data: Mapped[str] = mapped_column(Text, nullable=False)

    # Timestamp when the session was created. Using optional so that existing
    # rows without a value (e.g., before this field was introduced) are still
    # mapped correctly. A default of the current UTC time is supplied so
    # ``NULL`` values are avoided on insert.
    created_at: Mapped[Optional["datetime"]] = mapped_column(
        sa.DateTime(), nullable=True, default=sa.func.now()
    )

    # Timestamp when the session was last updated. This column should be
    # updated whenever the session is modified. A default of the current
    # UTC time is supplied to mirror ``created_at``.
    updated_at: Mapped[Optional["datetime"]] = mapped_column(
        sa.DateTime(), nullable=True, default=sa.func.now(), onupdate=sa.func.now()
    )