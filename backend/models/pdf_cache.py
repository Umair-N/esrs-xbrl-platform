"""
PDF Cache Model

Stores preprocessed PDF page data (word bounding boxes, images, and metadata) in the
database for persistence across backend restarts and horizontal scaling.
"""

import uuid
from sqlalchemy import String, Integer, Float, ForeignKey, UniqueConstraint, Index, LargeBinary
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from models.base import Base


class PDFCache(Base):
    __tablename__ = "pdf_cache"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Page dimensions
    page_width: Mapped[float] = mapped_column(Float, nullable=False)
    page_height: Mapped[float] = mapped_column(Float, nullable=False)

    # Word data stored as JSONB for efficient querying
    # Structure: {"words": [{"bbox": [x0,y0,x1,y1], "text": "...", "start_index": N, "end_index": M}]}
    words: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Page image as JPEG bytes for instant loading
    image: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)

    # Scale information (for potential multi-resolution support)
    scale: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    # Unique constraint: one cache entry per report/page/scale combination
    __table_args__ = (
        UniqueConstraint("report_id", "page_number", "scale", name="uq_pdf_cache_report_page_scale"),
        Index("idx_pdf_cache_report_page", "report_id", "page_number"),
    )

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "page_number": self.page_number,
            "page_width": self.page_width,
            "page_height": self.page_height,
            "words": self.words.get("words", []) if isinstance(self.words, dict) else [],
        }
