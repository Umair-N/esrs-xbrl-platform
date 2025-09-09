# services/context_service.py
from __future__ import annotations
from typing import Optional, Dict, Any, List
from datetime import date
import hashlib, json

from crud.context import context_crud
from schemas.context import XBRLContextCreate, XBRLContextUpdate, XBRLContextFilter


def _d2s(d: Optional[date]) -> str:
    return d.isoformat() if d else ""


def _canonical_hash(data: Dict[str, Any]) -> str:
    dims_norm = json.dumps(data.get("dimensions_json") or {}, sort_keys=True, separators=(",", ":"))
    parts = [
        data["entity_scheme"],
        data["entity_identifier"],
        data["period_type"],
        _d2s(data.get("start_date")),
        _d2s(data.get("end_date")),
        _d2s(data.get("instant_date")),
        dims_norm,
    ]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _validate_period(pt: str, start_date, end_date, instant_date):
    if pt == "instant":
        if not instant_date or start_date or end_date:
            raise ValueError("instant requires instant_date and no start/end")
    elif pt == "duration":
        if not start_date or not end_date or instant_date or end_date < start_date:
            raise ValueError("duration requires start_date <= end_date and no instant_date")
    elif pt == "forever":
        if any([start_date, end_date, instant_date]):
            raise ValueError("forever requires no dates")
    else:
        raise ValueError("invalid period_type")


def _normalize_vm_for_store(v):
    # Store as [] (never {}) to keep DB consistent
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return [] if not v else [v]
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return parsed
            if isinstance(parsed, dict):
                return [] if not parsed else [parsed]
        except Exception:
            return []
    return []


class ContextService:
    def create(self, dto: XBRLContextCreate, db, user_id: int):
        data = dto.model_dump()
        _validate_period(data["period_type"], data["start_date"], data["end_date"], data["instant_date"])
        data["content_hash"] = _canonical_hash(data)
        data["user_id"] = user_id
        data["validation_messages"] = _normalize_vm_for_store(data.get("validation_messages"))
        return context_crud.create(data, db)

    def bulk_create(self, items: List[XBRLContextCreate], db, user_id: int):
        rows: List[Dict[str, Any]] = []
        for dto in items:
            d = dto.model_dump()
            _validate_period(d["period_type"], d["start_date"], d["end_date"], d["instant_date"])
            d["content_hash"] = _canonical_hash(d)
            d["user_id"] = user_id
            d["validation_messages"] = _normalize_vm_for_store(d.get("validation_messages"))
            rows.append(d)
        return context_crud.bulk_upsert(rows, db)

    def get(self, ctx_id: int, db, user_id: int):
        return context_crud.get_by_id(ctx_id, user_id, db)

    def list(self, filters: XBRLContextFilter, db, user_id: int):
        return context_crud.list(filters.model_dump(), user_id, db)

    def update(self, ctx_id: int, dto: XBRLContextUpdate, db, user_id: int):
        data = dto.model_dump(exclude_unset=True)
        if "validation_messages" in data:
            data["validation_messages"] = _normalize_vm_for_store(data.get("validation_messages"))
        # entity/period changes are not allowed here by design; keeps content_hash stable
        return context_crud.update_partial(ctx_id, user_id, data, db)

    def delete(self, ctx_id: int, db, user_id: int) -> bool:
        return context_crud.delete(ctx_id, user_id, db)


context_service = ContextService()
