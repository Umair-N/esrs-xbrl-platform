# controllers/xbrl_context_controller.py
from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.context import (
    XBRLContextCreate, XBRLContextOut, XBRLContextFilter, XBRLContextUpdate
)
from services.context_service import context_service
from api.dep import get_db, get_current_user  # adjust import path if different
from models.user import User

router = APIRouter()


@router.post("", response_model=XBRLContextOut, status_code=status.HTTP_201_CREATED)
def create_context(
    body: XBRLContextCreate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        row = context_service.create(body, db, current_user.id)
        if not row:
            raise HTTPException(status_code=400, detail="Failed to create context")
        return row
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.post("/bulk", response_model=List[XBRLContextOut], status_code=status.HTTP_201_CREATED)
def bulk_create_contexts(
    body: List[XBRLContextCreate],
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return context_service.bulk_create(body, db, current_user.id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("", response_model=List[XBRLContextOut])
def list_contexts(
    filters: XBRLContextFilter = Depends(),
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return context_service.list(filters, db, current_user.id)


@router.get("/{context_id:int}", response_model=XBRLContextOut)
def get_context(
    context_id: int,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = context_service.get(context_id, db, current_user.id)
    if not row:
        raise HTTPException(status_code=404, detail="Context not found")
    return row


@router.patch("/{context_id:int}", response_model=XBRLContextOut)
def update_context(
    context_id: int,
    body: XBRLContextUpdate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = context_service.update(context_id, body, db, current_user.id)
    if not row:
        raise HTTPException(status_code=404, detail="Context not found or no changes")
    return row


@router.delete("/{context_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_context(
    context_id: int,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = context_service.delete(context_id, db, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Context not found")
    return
