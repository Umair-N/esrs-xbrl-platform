# models/xbrl_context.py
from __future__ import annotations

import enum
from datetime import date
from typing import Optional, Dict, Any, List

from sqlalchemy import (
    String, Date, DateTime, Boolean, Enum, Integer, JSON,
    Index, CheckConstraint, ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class PeriodType(enum.Enum):
    instant = "instant"
    duration = "duration"
    forever = "forever"


class ContextStatus(enum.Enum):
    valid = "valid"
    warning = "warning"
    error = "error"


class XBRLContext(Base):
    __tablename__ = "xbrl_contexts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # NEW: owner (scope contexts per user)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # XBRL <context> @id (not globally unique; we scope per user)
    context_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    # ---- Entity (who)
    entity_scheme: Mapped[str] = mapped_column(String(512), nullable=False)
    entity_identifier: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    lei: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)

    # ---- Period (when)
    period_type: Mapped[PeriodType] = mapped_column(Enum(PeriodType, name="xbrl_period_type"), nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    instant_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # ---- Dimensions (optional)
    dimensions_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # ---- Taxonomy (optional link to your table)
    taxonomy_id: Mapped[Optional[int]] = mapped_column(ForeignKey("taxonomies.id"), nullable=True, index=True)

    # ---- Integrity / validation
    # NOTE: no global unique here—uniques are per user (see __table_args__).
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    is_default_context: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[ContextStatus] = mapped_column(
        Enum(ContextStatus, name="xbrl_context_status"), nullable=False, default=ContextStatus.valid
    )
    validation_messages: Mapped[Optional[List[dict]]] = mapped_column(JSON, nullable=True)

    # ---- Timestamps
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        # enforce correct period/date combos
        CheckConstraint(
            "("
            " (period_type = 'instant'  AND instant_date IS NOT NULL AND start_date IS NULL AND end_date IS NULL)"
            " OR "
            " (period_type = 'duration' AND start_date IS NOT NULL AND end_date IS NOT NULL "
            "                           AND instant_date IS NULL AND end_date >= start_date)"
            " OR "
            " (period_type = 'forever'  AND instant_date IS NULL AND start_date IS NULL AND end_date IS NULL)"
            ")",
            name="ck_xc_period_fields"
        ),
        # common query pattern: entity + period
        Index("ix_xc_entity_period", "entity_identifier", "period_type", "start_date", "end_date", "instant_date"),
        # per-user uniqueness (prevents duplicate XML ids for a user)
        UniqueConstraint("user_id", "context_id", name="uq_ctx_id_per_user"),
        # per-user idempotent upsert by content
        UniqueConstraint("user_id", "content_hash", name="uq_ctx_hash_per_user"),
    )
