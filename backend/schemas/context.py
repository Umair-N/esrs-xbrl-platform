from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Dict, Any, List, Literal
from datetime import date, datetime
import json

PeriodType = Literal["instant", "duration", "forever"]
ContextStatus = Literal["valid", "warning", "error"]


def _normalize_validation_messages(v):
    """
    Accept None | list | dict | JSON string and coerce to a list.
    - None -> None (we keep None inbound, but coerce to [] when storing server-side)
    - [] stays []
    - {} -> []
    - {"code":"X"} -> [{"code":"X"}]
    - '[...]' / '{"..."}' (string) -> parsed then normalized
    """
    if v is None:
        return None
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return [] if not v else [v]
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
        except Exception:
            return None
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            return [] if not parsed else [parsed]
    return None


class XBRLContextBase(BaseModel):
    context_id: str = Field(..., max_length=128)
    entity_scheme: str = Field(..., max_length=512)
    entity_identifier: str = Field(..., max_length=128)
    entity_name: Optional[str] = Field(None, max_length=512)
    lei: Optional[str] = Field(None, max_length=20)

    period_type: PeriodType
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    instant_date: Optional[date] = None

    dimensions_json: Optional[Dict[str, Any]] = None
    taxonomy_id: Optional[int] = None

    is_default_context: bool = False
    status: ContextStatus = "valid"
    validation_messages: Optional[List[dict]] = None

    # Coerce validation_messages before validation/serialization
    @field_validator("validation_messages", mode="before")
    @classmethod
    def normalize_validation_messages(cls, v):
        return _normalize_validation_messages(v)

    # Early cross-field validation so callers get nice errors before hitting DB/service
    @model_validator(mode="after")
    def _check_period_fields(self):
        pt = self.period_type
        if pt == "instant":
            if not self.instant_date or self.start_date or self.end_date:
                raise ValueError("instant requires instant_date and no start/end")
        elif pt == "duration":
            if not self.start_date or not self.end_date or self.instant_date:
                raise ValueError("duration requires start_date & end_date and no instant_date")
            if self.end_date < self.start_date:
                raise ValueError("duration requires end_date >= start_date")
        elif pt == "forever":
            if any([self.start_date, self.end_date, self.instant_date]):
                raise ValueError("forever requires no dates")
        return self


class XBRLContextCreate(XBRLContextBase):
    # NOTE: user_id is set server-side from current_user.id
    pass


class XBRLContextUpdate(BaseModel):
    entity_name: Optional[str] = None
    lei: Optional[str] = None
    dimensions_json: Optional[Dict[str, Any]] = None
    taxonomy_id: Optional[int] = None
    is_default_context: Optional[bool] = None
    status: Optional[ContextStatus] = None
    validation_messages: Optional[List[dict]] = None

    @field_validator("validation_messages", mode="before")
    @classmethod
    def normalize_validation_messages(cls, v):
        return _normalize_validation_messages(v)


class XBRLContextOut(BaseModel):
    id: int
    user_id: int
    context_id: str
    entity_scheme: str
    entity_identifier: str
    entity_name: Optional[str]
    lei: Optional[str]
    period_type: PeriodType
    start_date: Optional[date]
    end_date: Optional[date]
    instant_date: Optional[date]
    dimensions_json: Optional[Dict[str, Any]]
    taxonomy_id: Optional[int]
    content_hash: str
    is_default_context: bool
    status: ContextStatus
    validation_messages: Optional[List[dict]]
    created_at: datetime
    updated_at: datetime

    # Normalize here too so responses never break
    @field_validator("validation_messages", mode="before")
    @classmethod
    def normalize_validation_messages(cls, v):
        return _normalize_validation_messages(v)

    class Config:
        from_attributes = True


class XBRLContextFilter(BaseModel):
    # NOTE: user scoping is handled in the controller/service from current_user.id.
    entity_identifier: Optional[str] = None
    period_type: Optional[PeriodType] = None
    taxonomy_id: Optional[int] = None
    context_id: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    is_default_context: Optional[bool] = None
    limit: int = 50
    offset: int = 0
