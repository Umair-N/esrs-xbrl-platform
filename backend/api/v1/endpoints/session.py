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
    import logging

    logger = logging.getLogger(__name__)
    logger.info(f"Creating session for user {current_user.id} with name: {session.name}")

    try:
        # Serialize the session data to JSON string, with default handling for non-serializable types
        data_json = json.dumps(session.data, default=str, ensure_ascii=False)
        logger.debug(f"Serialized data length: {len(data_json)} characters")
    except (TypeError, ValueError) as e:
        logger.error(f"JSON serialization error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid session data format: {str(e)}",
        )

    try:
        row = session_crud.create_session(
            user_id=current_user.id,
            name=session.name,
            data=data_json,
            db=db,
        )
        logger.info(f"Session created successfully with ID: {row['id']}")
    except Exception as e:
        logger.error(f"Database error while creating session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}",
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

    try:
        # Serialize the session data to JSON string, with default handling for non-serializable types
        data_json = json.dumps(session.data, default=str, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid session data format: {str(e)}",
        )

    try:
        row = session_crud.update_session(
            session_id=session_id,
            user_id=current_user.id,
            name=session.name,
            data=data_json,
            db=db,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session: {str(e)}",
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