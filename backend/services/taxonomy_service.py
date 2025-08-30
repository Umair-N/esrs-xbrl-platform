import os
import shutil
from typing import Any, Dict, List, Optional

from crud.taxonomy import taxonomy_crud 


class TaxonomyService:
    def __init__(self):
        # The base directory for taxonomies should be relative to the project root
        self.crud = taxonomy_crud
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the current directory of the script
        self.TAXONOMY_DIR = os.path.join(self.BASE_DIR, "../output/taxonomies")

        print(f"TaxonomyService: using TAXONOMY_DIR={self.TAXONOMY_DIR}")
        os.makedirs(self.TAXONOMY_DIR, exist_ok=True)

    # ------- Catalog -------
    def list_taxonomies(self, *, db) -> List[Dict[str, Any]]:
        return self.crud.list_taxonomies(db)

    def upload_taxonomy(self, *, name: str, upload_file, created_by: Optional[int], db) -> Dict[str, Any]:
        base = os.path.basename(upload_file.filename)
        
        # Check if the file is a valid .zip file
        if not base.lower().endswith(".zip"):
            raise ValueError("Only .zip files are allowed")
        
        # Generate a platform-independent path for the file
        # Join the taxonomy directory with the filename
        dest = os.path.join(self.TAXONOMY_DIR, base)
        
        with open(dest, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)

        # Ensure uniqueness by checking the filename in the database
        existing = [t for t in self.crud.list_taxonomies(db) if t["file_name"] == base]
        if existing:
            raise ValueError("A taxonomy with this file_name already exists")

        # Store the file with a relative path in the database
        # Use os.path.relpath to make sure the path is relative to the base directory
        file_path_relative = os.path.relpath(dest, self.BASE_DIR)

        return self.crud.create_taxonomy(name=name, file_name=base, file_path=file_path_relative, created_by=created_by, db=db)

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
    
    def get_user_taxonomies(self, user_id: int, db):
        """
        Get all taxonomies assigned to a user (including active and inactive).
        """
        return self.crud.get_user_taxonomies(user_id, db)

    def switch_taxonomy(self, user_id: int, taxonomy_id: int, db) -> Dict[str, str]:
        """
        Switch the active taxonomy for a user.
        1. Disables all taxonomies for the user.
        2. Enables the selected taxonomy.
        """
        return self.crud.switch_taxonomy(user_id, taxonomy_id, db)


# singleton-ish service instance
taxonomy_service = TaxonomyService()
