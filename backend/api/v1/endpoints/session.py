from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from api.dep import get_current_user
from database.session import get_db
from models.user import User
from crud.session import session_crud
from schemas.session import SessionCreate, SessionSummary, EditorSessionResponse

router = APIRouter()


@router.get("", response_model=List[SessionSummary])
async def list_sessions(
    current_user: User = Depends(get_current_user), db=Depends(get_db)
):
    """
    Return all editor sessions belonging to the current user. The payload does
    not include the full session data to reduce payload size.
    """
    rows = session_crud.get_sessions_by_user(current_user.id, db)
    return [
        SessionSummary(
            id=str(row["id"]),
            name=row["name"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )
        for row in rows
    ]


@router.get("/{session_id}", response_model=EditorSessionResponse)
async def read_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Fetch a single session by ID. Only the owner may retrieve the session.
    """
    row = session_crud.get_session_by_id(session_id, current_user.id, db)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    # 'data' is stored as JSON string, so attempt to parse. If parsing fails
    # return the raw string.
    import json

    try:
        parsed = json.loads(row["data"])
    except Exception:
        parsed = row["data"]
    return EditorSessionResponse(
        id=str(row["id"]),
        name=row["name"],
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
        data=parsed,
    )


@router.post("", response_model=EditorSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session: SessionCreate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Persist a new editor session for the current user. The session payload
    should include a name and the session data (report document).
    """
    import json

    row = session_crud.create_session(
        user_id=current_user.id,
        name=session.name,
        data=json.dumps(session.data),
        db=db,
    )
    return EditorSessionResponse(
        id=str(row["id"]),
        name=row["name"],
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
        data=session.data,
    )


@router.put("/{session_id}", response_model=EditorSessionResponse)
async def update_session(
    session_id: str,
    session: SessionCreate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Update an existing editor session. Only the owner can update the session.
    """
    import json

    row = session_crud.update_session(
        session_id=session_id,
        user_id=current_user.id,
        name=session.name,
        data=json.dumps(session.data),
        db=db,
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return EditorSessionResponse(
        id=str(row["id"]),
        name=row["name"],
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
        data=session.data,
    )