from __future__ import annotations

import os
import shutil
from typing import Any, Dict, List, Optional

from crud.taxonomy import taxonomy_crud


class TaxonomyService:
    def __init__(self):
        self.crud = taxonomy_crud
        self.TAXONOMY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output/taxonomies"))
        os.makedirs(self.TAXONOMY_DIR, exist_ok=True)

    # ------- Catalog -------
    def list_taxonomies(self, *, db) -> List[Dict[str, Any]]:
        return self.crud.list_taxonomies(db)

    def upload_taxonomy(self, *, name: str, upload_file, created_by: Optional[int], db) -> Dict[str, Any]:
        base = os.path.basename(upload_file.filename)
        if not base.lower().endswith(".zip"):
            raise ValueError("Only .zip files are allowed")
        dest = os.path.join(self.TAXONOMY_DIR, base)
        with open(dest, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)

        # Ensure uniqueness by file_name
        existing = [t for t in self.crud.list_taxonomies(db) if t["file_name"] == base]
        if existing:
            raise ValueError("A taxonomy with this file_name already exists")

        return self.crud.create_taxonomy(name=name, file_name=base, file_path=dest, created_by=created_by, db=db)

    def set_taxonomy_enabled(self, *, taxonomy_id: int, enabled: bool, db) -> None:
        self.crud.set_taxonomy_enabled(taxonomy_id=taxonomy_id, enabled=enabled, db=db)

    # ------- Assignments -------
    def assign_user_taxonomy(self, *, user_id: int, taxonomy_id: int, set_by: Optional[int], db) -> None:
        self.crud.set_user_active_taxonomy(user_id=user_id, taxonomy_id=taxonomy_id, set_by=set_by, db=db)

    def disable_user_taxonomy(self, *, user_id: int, db) -> int:
        return self.crud.disable_user_taxonomy(user_id=user_id, db=db)

    # ------- Resolve -------
    def resolve_active_taxonomy_path(self, *, user_id: int, db) -> str:
        return self.crud.resolve_active_taxonomy_path(user_id=user_id, db=db)

    def get_user_active_taxonomy(self, *, user_id: int, db) -> Optional[Dict[str, Any]]:
        return self.crud.get_user_active_taxonomy(user_id=user_id, db=db)


# singleton-ish service instance
taxonomy_service = TaxonomyService()
