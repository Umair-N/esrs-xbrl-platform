from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException, status

from api.dep import get_current_user
from database.session import get_db
from crud.canvas import canvas_crud
from schemas.canvas import CanvasCreate, CanvasResponse

router = APIRouter()


@router.post("", response_model=CanvasResponse, status_code=status.HTTP_201_CREATED)
async def create_canvas_state(
    canvas: CanvasCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Persist a new canvas state for the authenticated user. The client
    submits a fully serialized report document via the ``data`` field.
    An optional ``name`` can be supplied to aid in display. The newly
    created canvas ID is returned along with the stored data.
    """
    import json

    try:
        row = canvas_crud.create_canvas(
            user_id=current_user.id,
            name=canvas.name,
            data=json.dumps(canvas.data),
            report_id=canvas.report_id,
            db=db,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save canvas: {exc}",
        )
    # Convert JSON back to Python object for response
    try:
        parsed = json.loads(row["data"])
    except Exception:
        parsed = row["data"]
    return CanvasResponse(
        id=str(row["id"]),
        name=row.get("name"),
        data=parsed,
        report_id=row.get("report_id"),
        user_id=row.get("user_id"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


@router.get("/{canvas_id}", response_model=CanvasResponse)
async def get_canvas_state(
    canvas_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Retrieve a previously saved canvas state by ID. Only the owner of
    the canvas may fetch it. The stored JSON is deserialized before
    being returned to the client.
    """
    import json

    row = canvas_crud.get_canvas_by_id(canvas_id, current_user.id, db)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas not found",
        )
    try:
        parsed = json.loads(row["data"])
    except Exception:
        parsed = row["data"]
    return CanvasResponse(
        id=str(row["id"]),
        name=row.get("name"),
        data=parsed,
        report_id=row.get("report_id"),
        user_id=row.get("user_id"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


@router.get("", response_model=List[CanvasResponse])
async def list_canvas_states(
    limit: int = 100,
    offset: int = 0,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    List all canvases for the authenticated user. Results are ordered by
    ``updated_at`` descending. Pagination parameters ``limit`` and
    ``offset`` allow clients to page through large result sets.
    """
    import json

    rows = canvas_crud.list_canvases(current_user.id, db, limit=limit, offset=offset)
    canvases: List[CanvasResponse] = []
    for row in rows:
        try:
            parsed = json.loads(row["data"])
        except Exception:
            parsed = row["data"]
        canvases.append(
            CanvasResponse(
                id=str(row["id"]),
                name=row.get("name"),
                data=parsed,
                report_id=row.get("report_id"),
                user_id=row.get("user_id"),
                created_at=row.get("created_at"),
                updated_at=row.get("updated_at"),
            )
        )
    return canvases


@router.put("/{canvas_id}", response_model=CanvasResponse)
async def update_canvas_state(
    canvas_id: str,
    canvas: CanvasCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Update an existing canvas owned by the authenticated user. Only the
    ``name``, ``data``, and ``report_id`` fields are modifiable.
    """
    import json

    try:
        row = canvas_crud.update_canvas(
            canvas_id=canvas_id,
            user_id=current_user.id,
            name=canvas.name,
            data=json.dumps(canvas.data),
            report_id=canvas.report_id,
            db=db,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update canvas: {exc}",
        )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas not found",
        )
    try:
        parsed = json.loads(row["data"])
    except Exception:
        parsed = row["data"]
    return CanvasResponse(
        id=str(row["id"]),
        name=row.get("name"),
        data=parsed,
        report_id=row.get("report_id"),
        user_id=row.get("user_id"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
    )


@router.delete("/{canvas_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_canvas_state(
    canvas_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Delete a saved canvas state. Returns 204 on success or 404 if the
    canvas does not exist or belongs to another user.
    """
    deleted = canvas_crud.delete_canvas(canvas_id, current_user.id, db)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Canvas not found",
        )
    return