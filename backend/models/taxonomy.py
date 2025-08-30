# models/taxonomy.py
from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, func, UniqueConstraint, Index, text
from models.base import Base  # your existing Base

class Taxonomy(Base):
    __tablename__ = "taxonomies"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Display name you choose (e.g., "Finance v3")
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    # The zip filename on disk (e.g., "finance_v3.zip")
    file_name: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    # Absolute path you will stream from
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Optional: backref to assignments
    assignments: Mapped[list["UserTaxonomy"]] = relationship(back_populates="taxonomy", cascade="all, delete-orphan")

class UserTaxonomy(Base):
    __tablename__ = "user_taxonomies"

    user_id: Mapped[int] = mapped_column(nullable=False)
    taxonomy_id: Mapped[int] = mapped_column(ForeignKey("taxonomies.id", ondelete="CASCADE"), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    set_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        # Remove the unique constraint for one active taxonomy per user.
        UniqueConstraint("user_id", "taxonomy_id", name="user_taxonomies_user_taxonomy_uniq"),
    )

    # Optional index to ensure fast lookups for active taxonomies
    Index(
        "user_taxonomies_one_active_per_user",
        "user_id",
        unique=False,
        postgresql_where=text("enabled = TRUE"),
    )

    taxonomy: Mapped["Taxonomy"] = relationship(back_populates="assignments")
