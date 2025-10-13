import uuid
from typing import Optional

# Import the datetime type so that SQLAlchemy can resolve annotations
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class CanvasState(Base):
    """
    Represents a persisted canvas/editor state. This model stores the
    serialized report (canvas) data along with optional metadata. Each
    canvas record is associated with a user so multiple users can save
    their own versions of the same underlying report.

    The ``data`` column holds the full report JSON as a string. Using
    ``Text`` rather than a dedicated JSON type allows the application
    to remain database‑agnostic while still storing arbitrarily complex
    structures. Timestamps track when the canvas was created and last
    updated.
    """

    __tablename__ = "canvas_states"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Optionally reference the original uploaded report. This is stored
    # as a string because upstream report identifiers are UUIDs cast to
    # strings. It may be null if the canvas was created without an
    # underlying upload.
    report_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Associate the canvas with the user who created it. While not
    # strictly required by the specification, tying canvas states to
    # users ensures one person's saved reports remain private. If the
    # application evolves to support shared documents, this field can
    # be adjusted accordingly.
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )

    # Optional human‑friendly name for the saved canvas. Defaults to
    # ``None``. Frontend clients can supply a descriptive title or
    # repurpose the original report's title.
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Persist the full canvas/report JSON as a string. Text is used
    # instead of a JSON type to remain compatible across different
    # database backends (e.g. SQLite, PostgreSQL). Clients should
    # serialize their data to JSON before storing it in this column.
    data: Mapped[str] = mapped_column(Text, nullable=False)

    # Timestamp when the canvas was first saved. Using ``nullable=True``
    # here ensures existing rows created before this column was added
    # remain valid. A default of the current UTC time is supplied so
    # ``NULL`` values are avoided on insert.
    created_at: Mapped[Optional[datetime]] = mapped_column(
        sa.DateTime(), nullable=True, default=sa.func.now()
    )

    # Timestamp when the canvas was last modified. This field is
    # automatically updated whenever the row is updated. As with
    # ``created_at``, ``nullable=True`` preserves compatibility with
    # legacy rows.
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        sa.DateTime(), nullable=True, default=sa.func.now(), onupdate=sa.func.now()
    )