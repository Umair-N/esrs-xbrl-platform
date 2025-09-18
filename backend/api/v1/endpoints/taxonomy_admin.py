from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from psycopg2.extensions import connection as PGConnection

from api.dep import get_db, get_current_user, require_admin
from services.taxonomy_service import taxonomy_service
from schemas.taxonomy import TaxonomyRequestBody

taxonomy_admin = APIRouter(prefix="/taxonomy/admin", tags=["taxonomy-admin"])


@taxonomy_admin.get("/list")
def list_taxonomies(db: PGConnection = Depends(get_db), _: Any = Depends(require_admin)) -> List[Dict[str, Any]]:
    return taxonomy_service.list_taxonomies(db=db)


@taxonomy_admin.post("/upload")
def upload_taxonomy(
    name: str = Query(..., description="Display name"),
    file: UploadFile = File(...),
    db: PGConnection = Depends(get_db),
    admin=Depends(require_admin),
):
    try:
        row = taxonomy_service.upload_taxonomy(name=name, upload_file=file, created_by=getattr(admin, "id", None), db=db)
        return row
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@taxonomy_admin.post("/taxonomies/{taxonomy_id}/enable")
def enable_taxonomy(taxonomy_id: int, db: PGConnection = Depends(get_db), _: Any = Depends(require_admin)):
    try:
        taxonomy_service.set_taxonomy_enabled(taxonomy_id=taxonomy_id, enabled=True, db=db)
        return {"message": "Enabled"}
    except ValueError:
        raise HTTPException(404, detail="Taxonomy not found")


@taxonomy_admin.post("/taxonomies/{taxonomy_id}/disable")
def disable_taxonomy(taxonomy_id: int, db: PGConnection = Depends(get_db), _: Any = Depends(require_admin)):
    try:
        taxonomy_service.set_taxonomy_enabled(taxonomy_id=taxonomy_id, enabled=False, db=db)
        return {"message": "Disabled"}
    except ValueError:
        raise HTTPException(404, detail="Taxonomy not found")


@taxonomy_admin.patch("/users/{user_id}/set-active")
def set_user_taxonomy(
    user_id: int,
    body: TaxonomyRequestBody,  
    db: PGConnection = Depends(get_db),
    admin=Depends(require_admin),
):
    try:
        for taxonomy_id in body.taxonomy_ids:
            taxonomy_service.assign_user_taxonomy(
                user_id=user_id, taxonomy_id=taxonomy_id, set_by=getattr(admin, "id", None), db=db
            )
        return {"message": f"Taxonomies {body.taxonomy_ids} are now active for user {user_id}"}
    except ValueError as e:
        raise HTTPException(404, detail=str(e))

@taxonomy_admin.post("/users/{user_id}/disable")
def disable_user_taxonomy(user_id: int, db: PGConnection = Depends(get_db), _: Any = Depends(require_admin)):
    count = taxonomy_service.disable_user_taxonomy(user_id=user_id, db=db)
    return {"message": f"Disabled {count} active mapping(s) for user {user_id}"}
