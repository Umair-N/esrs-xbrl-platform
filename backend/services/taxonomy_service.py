import os
import shutil
import tempfile
import logging
from typing import Any, Dict, List, Optional

from crud.taxonomy import taxonomy_crud 
from core.config import get_settings

logger = logging.getLogger(__name__)


class TaxonomyService:
    def __init__(self):
        self.crud = taxonomy_crud
        self.settings = get_settings()
        
        # Always set BASE_DIR for consistency
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Debug logging
        print(f"TaxonomyService initialization:")
        print(f"  GOOGLE_CLOUD_PROJECT: {self.settings.GOOGLE_CLOUD_PROJECT}")
        print(f"  GAE_ENV: {self.settings.GAE_ENV}")
        print(f"  ENVIRONMENT: {self.settings.ENVIRONMENT}")
        print(f"  is_gcp_deployment: {self.settings.is_gcp_deployment}")
        
        if self.settings.is_gcp_deployment:
            # On GCP, use a writable temp directory
            self.TAXONOMY_DIR = os.path.join(tempfile.gettempdir(), "taxonomies")
            logger.info(f"GCP deployment detected, using temp dir: {self.TAXONOMY_DIR}")
        else:
            # Local development
            self.TAXONOMY_DIR = os.path.join(self.BASE_DIR, "..", "output", "taxonomies")
            self.TAXONOMY_DIR = os.path.abspath(self.TAXONOMY_DIR)
            logger.info(f"Local development, using: {self.TAXONOMY_DIR}")
        
        print(f"  Final TAXONOMY_DIR: {self.TAXONOMY_DIR}")
        
        # Ensure directory exists and is writable
        try:
            os.makedirs(self.TAXONOMY_DIR, exist_ok=True)
            # Test write permissions
            test_file = os.path.join(self.TAXONOMY_DIR, ".write_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            logger.info(f"TaxonomyService initialized successfully: {self.TAXONOMY_DIR}")
        except Exception as e:
            logger.error(f"Failed to create or write to taxonomy directory: {e}")
            if self.settings.is_gcp_deployment:
                # Fallback to system temp directory on GCP
                self.TAXONOMY_DIR = tempfile.mkdtemp(prefix="taxonomies_")
                logger.info(f"Using fallback temp directory: {self.TAXONOMY_DIR}")

    # ------- Catalog -------
    def list_taxonomies(self, *, db) -> List[Dict[str, Any]]:
        return self.crud.list_taxonomies(db)

    def upload_taxonomy(self, *, name: str, upload_file, created_by: Optional[int], db) -> Dict[str, Any]:
        base = os.path.basename(upload_file.filename)
        
        # Check if the file is a valid .zip file
        if not base.lower().endswith(".zip"):
            raise ValueError("Only .zip files are allowed")
        
        # Ensure uniqueness by checking the filename in the database first
        existing = [t for t in self.crud.list_taxonomies(db) if t["file_name"] == base]
        if existing:
            raise ValueError("A taxonomy with this file_name already exists")
        
        # Generate the destination path
        dest = os.path.join(self.TAXONOMY_DIR, base)
        
        try:
            # Reset file pointer and copy file
            upload_file.file.seek(0)
            with open(dest, "wb") as f:
                shutil.copyfileobj(upload_file.file, f)
            
            logger.info(f"File uploaded successfully to: {dest}")
            
            # Store path differently based on environment
            if self.settings.is_gcp_deployment:
                # On GCP, store the absolute path since temp directories can vary
                file_path_to_store = dest
            else:
                # Local development - store relative path
                file_path_to_store = os.path.relpath(dest, self.BASE_DIR)
            
            return self.crud.create_taxonomy(
                name=name, 
                file_name=base, 
                file_path=file_path_to_store, 
                created_by=created_by, 
                db=db
            )
            
        except Exception as e:
            logger.error(f"Failed to upload taxonomy file: {e}")
            raise ValueError(f"Failed to save file: {str(e)}")

    def set_taxonomy_enabled(self, *, taxonomy_id: int, enabled: bool, db) -> None:
        self.crud.set_taxonomy_enabled(taxonomy_id=taxonomy_id, enabled=enabled, db=db)

    # ------- Assignments -------
    def assign_user_taxonomy(self, *, user_id: int, taxonomy_id: int, set_by: Optional[int], db) -> None:
        self.crud.set_user_active_taxonomy(user_id=user_id, taxonomy_id=taxonomy_id, set_by=set_by, db=db)

    def disable_user_taxonomy(self, *, user_id: int, db) -> int:
        return self.crud.disable_user_taxonomy(user_id=user_id, db=db)

    # ------- Resolve -------
    def resolve_active_taxonomy_path(self, *, user_id: int, db) -> str:
        """
        Resolve the absolute path to the active taxonomy file for a user.
        Returns an absolute path that can be used to access the file.
        """
        stored_path = self.crud.resolve_active_taxonomy_path(user_id=user_id, db=db)
        if not stored_path:
            return ""
        
        try:
            if self.settings.is_gcp_deployment:
                # On GCP, we store absolute paths, so use them directly
                if os.path.isabs(stored_path) and os.path.exists(stored_path):
                    logger.info(f"Resolved taxonomy path for user {user_id}: {stored_path}")
                    return stored_path
                else:
                    # Fallback: try to construct path in current taxonomy directory
                    filename = os.path.basename(stored_path)
                    fallback_path = os.path.join(self.TAXONOMY_DIR, filename)
                    if os.path.exists(fallback_path):
                        logger.info(f"Using fallback path for user {user_id}: {fallback_path}")
                        return fallback_path
                    else:
                        logger.error(f"Taxonomy file not found for user {user_id}: {stored_path}")
                        return ""
            else:
                # Local development - handle relative paths
                if os.path.isabs(stored_path):
                    return stored_path if os.path.exists(stored_path) else ""
                
                parent_dir = os.path.dirname(self.BASE_DIR)
                absolute_path = os.path.join(parent_dir, stored_path)
                absolute_path = os.path.normpath(os.path.abspath(absolute_path))
                
                logger.info(f"Resolved taxonomy path for user {user_id}: {absolute_path}")
                return absolute_path if os.path.exists(absolute_path) else ""
                
        except Exception as e:
            logger.error(f"Error resolving taxonomy path for user {user_id}: {e}")
            return ""

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

    def cleanup_temp_files(self):
        """Clean up temporary files (useful for GCP where temp files might accumulate)"""
        if self.settings.is_gcp_deployment:
            try:
                import time
                current_time = time.time()
                for filename in os.listdir(self.TAXONOMY_DIR):
                    filepath = os.path.join(self.TAXONOMY_DIR, filename)
                    if os.path.isfile(filepath) and filename.endswith('.zip'):
                        file_age = current_time - os.path.getctime(filepath)
                        if file_age > 86400:  # 24 hours
                            os.remove(filepath)
                            logger.info(f"Cleaned up old file: {filepath}")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")

    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the taxonomy service configuration"""
        return {
            "is_gcp": self.settings.is_gcp_deployment,
            "environment": self.settings.ENVIRONMENT,
            "google_cloud_project": self.settings.GOOGLE_CLOUD_PROJECT,
            "taxonomy_dir": self.TAXONOMY_DIR,
            "dir_exists": os.path.exists(self.TAXONOMY_DIR),
            "dir_writable": os.access(self.TAXONOMY_DIR, os.W_OK) if os.path.exists(self.TAXONOMY_DIR) else False,
            "files_count": len([f for f in os.listdir(self.TAXONOMY_DIR) if f.endswith('.zip')]) if os.path.exists(self.TAXONOMY_DIR) else 0
        }


# singleton-ish service instance
taxonomy_service = TaxonomyService()