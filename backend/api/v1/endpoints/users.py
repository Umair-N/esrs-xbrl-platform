from typing import Optional
from fastapi import Query

from api.dep import get_current_user, require_admin
from database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Request
from models.user import User
from schemas.user import UserResponse, UserUpdate
from services.user_service import user_service
from datetime import datetime, timezone
from math import ceil
from fastapi.responses import JSONResponse
router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user), db=Depends(get_db)):

    now_utc = datetime.now(timezone.utc)

    user_service.update_user(user_id=current_user.id, user_data=UserUpdate(last_accessed_at=now_utc), db=db)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        role=current_user.role,
        created_at=current_user.created_at,
        company=current_user.company,
        designation=current_user.designation,
        last_accessed_at=current_user.last_accessed_at,
        last_login=current_user.last_login,
        platform_access=current_user.platform_access,
        status=current_user.status,
        updated_at=current_user.updated_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    limited_update = UserUpdate(full_name=user_update.full_name)

    updated_user = user_service.update_user(current_user.id, limited_update, db)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        full_name=updated_user.full_name,
        is_active=updated_user.is_active,
        is_verified=updated_user.is_verified,
        role=updated_user.role,
        created_at=updated_user.created_at,
    )

@router.get("", response_model=dict)
async def get_all_users(
    request: Request,
    admin_user: User = Depends(require_admin),
    db = Depends(get_db),
    page: int = Query(1, ge=1),  
    limit: int = Query(10, gt=0, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    search: Optional[str] = None
):
    skip = (page - 1) * limit

    query_params = dict(request.query_params)
    known_params = {"page", "limit", "sort_by", "sort_order", "search"}
    filters = {k: v for k, v in query_params.items() if k not in known_params}

    total_users = user_service.count_users(db, search=search, filters=filters)
    users = user_service.get_all_users(
        db=db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
        filters=filters
    )

    return {
        "total": total_users,
        "page": page,
        "pages": ceil(total_users / limit) if total_users > 0 else 0,
        "limit": limit,
        "users": [UserResponse(**user.__dict__) for user in users]
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int, admin_user: User = Depends(require_admin), db=Depends(get_db)
):
    user = user_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_verified=user.is_verified,
        role=user.role,
        created_at=user.created_at,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    admin_user: User = Depends(require_admin),
    db=Depends(get_db),
):
    updated_user = user_service.update_user(user_id, user_update, db)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        full_name=updated_user.full_name,
        is_active=updated_user.is_active,
        is_verified=updated_user.is_verified,
        role=updated_user.role,
        created_at=updated_user.created_at,
    )

@router.put("/{user_id}/grant-access")
async def grant_platform_access(user_id: int, admin_user: User = Depends(require_admin), db=Depends(get_db)):
    user_service.grant_access(user_id, db)
    response = JSONResponse(
        content={
            "message": "Platform access granted successfully",
        }
    )
    return response

@router.put("/{user_id}/revoke-access")
async def revoke_platform_access(user_id: int, admin_user: User = Depends(require_admin), db=Depends(get_db)):
    user_service.revoke_access(user_id, db)
    response = JSONResponse(
        content={
            "message": "Platform access revoked successfully",
        }
    )
    return response

@router.put("/{user_id}/enable")
async def enable_user(user_id: int, admin_user: User = Depends(require_admin), db=Depends(get_db)):
    user_service.enable(user_id, db)
    response = JSONResponse(
        content={
            "message": "User enabled successfully",
        }
    )
    return response

@router.put("/{user_id}/disable")
async def disable_user(user_id: int, admin_user: User = Depends(require_admin), db=Depends(get_db)):
    user_service.disable(user_id, db)
    response = JSONResponse(
        content={
            "message": "User disabled successfully",
        }
    )
    return response

