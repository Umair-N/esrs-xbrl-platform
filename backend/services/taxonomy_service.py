"""
TaxonomyService with optional Google Cloud Storage (GCS) support.

This implementation stores taxonomy ZIP archives either in the local
filesystem (during development) or in a GCS bucket (during production on
GCP).  The behaviour is controlled via configuration settings:

* ``STORAGE_BACKEND``: either ``"local"`` or ``"gcs"``.  If ``"gcs"``
  the service uploads files to the bucket specified by ``GCS_BUCKET``.
* ``GCS_BUCKET``: the name of the Cloud Storage bucket where taxonomy
  files should live.  Required when ``STORAGE_BACKEND="gcs"``.
* ``GCS_PREFIX``: optional prefix within the bucket for storing files
  (e.g. ``"taxonomies/"``).

The class automatically detects the deployment environment via
``settings.is_gcp_deployment`` and defaults to GCS storage if running in
GCP unless overridden by ``STORAGE_BACKEND``.  Uploaded files are
recorded in the database with either a filename (local mode) or a
``gs://`` URI (GCS mode).  When resolving a taxonomy path, GCS URIs
are downloaded into the taxonomy cache directory on first access.

Before using this service you must ensure that the Google Cloud client
library ``google-cloud-storage`` is installed and that the environment
is authenticated via either Application Default Credentials (ADC) or
explicit service account credentials (e.g. by setting the
``GOOGLE_APPLICATION_CREDENTIALS`` environment variable).  The service
account used must have read and write access to the bucket.
"""

import os
import shutil
import tempfile
import logging
from typing import Any, Dict, List, Optional

from crud.taxonomy import taxonomy_crud
from core.config import get_settings

logger = logging.getLogger(__name__)


try:
    from google.cloud import storage  # type: ignore
except ImportError:
    # If google-cloud-storage is not installed, users must install it when
    # enabling GCS storage.  Import lazily to avoid raising during local
    # development when the package may not be available.
    storage = None


class TaxonomyService:
    def __init__(self):
        self.crud = taxonomy_crud
        self.settings = get_settings()

        # Determine storage backend: override to 'gcs' if we are on GCP and
        # no explicit backend is provided
        backend = getattr(self.settings, "STORAGE_BACKEND", None)
        if backend is None:
            backend = "gcs" if self.settings.is_gcp_deployment else "local"
        self.storage_backend = backend.lower()

        # Base directory used for resolving local relative paths.  In local
        # development we use the current working directory; on GCP this
        # value is not used for storage but may be used to resolve legacy
        # relative paths.
        self.BASE_DIR = os.getcwd()

        # Directory used to store files locally and to cache downloaded GCS
        # objects.  On GCP we still use a temporary directory for caching
        # downloaded objects.
        if self.settings.is_gcp_deployment:
            self.TAXONOMY_DIR = os.path.join(tempfile.gettempdir(), "taxonomies")
        else:
            self.TAXONOMY_DIR = os.path.abspath(os.path.join(self.BASE_DIR, "output", "taxonomies"))
        os.makedirs(self.TAXONOMY_DIR, exist_ok=True)

        # GCS configuration
        self.gcs_bucket_name: Optional[str] = getattr(self.settings, "GCS_BUCKET", None)
        self.gcs_prefix: str = getattr(self.settings, "GCS_PREFIX", "") or ""
        if self.gcs_prefix and not self.gcs_prefix.endswith("/"):
            self.gcs_prefix += "/"

        if self.storage_backend == "gcs" and not self.gcs_bucket_name:
            raise ValueError(
                "GCS storage selected but GCS_BUCKET not configured. Set GCS_BUCKET in your settings or environment."
            )

    # ------- Catalog -------
    def list_taxonomies(self, *, db) -> List[Dict[str, Any]]:
        return self.crud.list_taxonomies(db)

    def upload_taxonomy(
        self, *, name: str, upload_file, created_by: Optional[int], db
    ) -> Dict[str, Any]:
        base = os.path.basename(upload_file.filename)
        if not base.lower().endswith(".zip"):
            raise ValueError("Only .zip files are allowed")

        # Check for duplicates
        existing = [t for t in self.crud.list_taxonomies(db) if t["file_name"] == base]
        if existing:
            raise ValueError("A taxonomy with this file_name already exists")

        # Upload to the appropriate backend
        if self.storage_backend == "gcs":
            if storage is None:
                raise RuntimeError(
                    "google-cloud-storage library is not installed. Install it to use GCS storage."
                )
            # Compose destination blob name with optional prefix
            dest_blob_name = self.gcs_prefix + base
            # Use existing file handle for upload
            upload_file.file.seek(0)
            client = storage.Client()
            bucket = client.bucket(self.gcs_bucket_name)
            blob = bucket.blob(dest_blob_name)
            blob.upload_from_file(upload_file.file)
            file_path_to_store = f"gs://{self.gcs_bucket_name}/{dest_blob_name}"
            logger.info(f"Uploaded taxonomy file to GCS at {file_path_to_store}")
        else:
            # Local storage
            dest_path = os.path.join(self.TAXONOMY_DIR, base)
            upload_file.file.seek(0)
            with open(dest_path, "wb") as out_file:
                shutil.copyfileobj(upload_file.file, out_file)
            file_path_to_store = base
            logger.info(f"Uploaded taxonomy file locally at {dest_path}")

        return self.crud.create_taxonomy(
            name=name,
            file_name=base,
            file_path=file_path_to_store,
            created_by=created_by,
            db=db,
        )

    def set_taxonomy_enabled(self, *, taxonomy_id: int, enabled: bool, db) -> None:
        self.crud.set_taxonomy_enabled(taxonomy_id=taxonomy_id, enabled=enabled, db=db)

    # ------- Assignments -------
    def assign_user_taxonomy(
        self, *, user_id: int, taxonomy_id: int, set_by: Optional[int], db
    ) -> None:
        self.crud.set_user_active_taxonomy(user_id=user_id, taxonomy_id=taxonomy_id, set_by=set_by, db=db)

    def disable_user_taxonomy(self, *, user_id: int, db) -> int:
        return self.crud.disable_user_taxonomy(user_id=user_id, db=db)

    # ------- Resolve -------
    def resolve_active_taxonomy_path(self, *, user_id: int, db) -> str:
        stored_path = self.crud.resolve_active_taxonomy_path(user_id=user_id, db=db)
        if not stored_path:
            return ""
        # If stored path is a GCS URI
        if stored_path.startswith("gs://"):
            if storage is None:
                raise RuntimeError(
                    "google-cloud-storage library is not installed. Install it to use GCS storage."
                )
            # Parse bucket and key
            try:
                _, rest = stored_path.split("gs://", 1)
                bucket_name, key = rest.split("/", 1)
            except ValueError:
                logger.error(f"Invalid GCS URI stored for user {user_id}: {stored_path}")
                return ""
            # Determine local cache path
            local_path = os.path.join(self.TAXONOMY_DIR, os.path.basename(key))
            # Download if not present
            if not os.path.exists(local_path):
                client = storage.Client()
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(key)
                # Ensure directory exists
                os.makedirs(self.TAXONOMY_DIR, exist_ok=True)
                blob.download_to_filename(local_path)
                logger.info(f"Downloaded taxonomy file from GCS to {local_path}")
            return local_path
        # If an absolute path is stored (legacy or local mode)
        if os.path.isabs(stored_path) and os.path.exists(stored_path):
            return stored_path
        # Try resolving relative paths (legacy)
        candidate = os.path.normpath(os.path.join(self.BASE_DIR, stored_path))
        if os.path.exists(candidate):
            return candidate
        # Finally treat stored_path as a filename in the local taxonomy dir
        fallback = os.path.join(self.TAXONOMY_DIR, os.path.basename(stored_path))
        if os.path.exists(fallback):
            return fallback
        return ""

    def get_user_active_taxonomy(
        self, *, user_id: int, db
    ) -> Optional[Dict[str, Any]]:
        return self.crud.get_user_active_taxonomy(user_id=user_id, db=db)

    def get_user_taxonomies(self, user_id: int, db):
        return self.crud.get_user_taxonomies(user_id, db)

    def switch_taxonomy(
        self, user_id: int, taxonomy_id: int, db
    ) -> Dict[str, str]:
        return self.crud.switch_taxonomy(user_id, taxonomy_id, db)


taxonomy_service = TaxonomyService()