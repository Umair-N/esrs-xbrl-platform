"""
Unified report service that delegates PDF preprocessing and caching
to the ``pdf_cache_service`` module.

This module exposes helper functions and a lightweight ``ReportService``
object for compatibility with existing imports.  All page metadata,
images and word data are managed by ``pdf_cache_service``, which
stores the processed pages in in-memory caches.  When a new PDF
report is created, preprocessing is scheduled using FastAPI's
``BackgroundTasks`` to avoid blocking the request.

The legacy ``report_service`` implementation contained its own
caching logic.  To reduce duplication and improve reliability, this
implementation forwards all page access calls to ``pdf_cache_service``.
It also provides a ``create_report`` method that schedules
preprocessing and returns a simple report-like object.
"""

from __future__ import annotations

from typing import Any, Optional, List, Dict
from fastapi import BackgroundTasks
import uuid
import os
from datetime import datetime

from .pdf_cache_service import (
    preprocess_pdf as cache_preprocess_pdf,
    get_page_info as cache_get_page_info,
    get_page_image as cache_get_page_image,
    get_page_words as cache_get_page_words,
)
from crud.report import ReportCRUD


class SimpleBlock:
    """A simple report block representation with attribute access.

    This class is used for storing blocks of text or other content
    associated with a report.  It provides attributes rather than
    dictionary keys so that existing code expecting dot-notation works.
    """

    def __init__(
        self,
        id: str,
        content: str,
        type: str,
        tags: list,
        order_index: int,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.content = content
        self.type = type
        self.tags = tags
        self.order_index = order_index
        self.created_at = created_at
        self.updated_at = updated_at


class SimpleReport:
    """A minimal report representation used for caching purposes.

    The application may define a full-fledged ``Report`` model in
    another module.  However, the caching layer only requires the
    ``id``, ``file_path`` and ``file_type`` attributes, so this
    lightweight class suffices for scheduling preprocessing.
    """

    def __init__(self, id: str, file_path: str, file_type: str) -> None:
        self.id = id
        self.file_path = file_path
        self.file_type = file_type
        # Additional attributes for compatibility with ReportResponse
        self.title: str = os.path.basename(file_path)
        self.file_size: int = 0
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None
        self.blocks: list | None = None
        self.user_id: Any | None = None


def create_report(
    file_path: str,
    file_type: str,
    report_id: str,
    background_tasks: Optional[BackgroundTasks] = None,
) -> SimpleReport:
    """Create a report and schedule PDF preprocessing.

    This helper instantiates a :class:`SimpleReport` and, if the
    uploaded file is a PDF, schedules asynchronous preprocessing via
    FastAPI's ``BackgroundTasks``.  The caller should store the
    returned report in persistent storage if necessary.

    :param file_path: Path to the uploaded file on disk.
    :param file_type: MIME type of the file (e.g. ``application/pdf``).
    :param report_id: Unique identifier for the report.
    :param background_tasks: Optional :class:`BackgroundTasks` for
        scheduling the preprocessing task.
    :return: A new :class:`SimpleReport` instance.
    """
    report = SimpleReport(report_id, file_path, file_type)
    # Populate default metadata
    report.file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    now = datetime.utcnow()
    report.created_at = now
    report.updated_at = now
    report.title = os.path.basename(file_path)
    # Schedule preprocessing for PDFs
    if file_type.lower().startswith("application/pdf") and background_tasks:
        # Use a wrapper to pass the report_id/file_path/file_type
        background_tasks.add_task(
            cache_preprocess_pdf,
            report_id=report.id,
            file_path=report.file_path,
            file_type=report.file_type,
            scale=1.0,
        )
    return report


# ---------------------------------------------------------------------------
# In-memory report registry for compatibility with original ReportService API.
# This is a simple placeholder to keep track of uploaded reports and allow
# retrieval via the ``report_service`` shim.  In a production system,
# these records should be persisted in a database instead.

_reports_by_user: Dict[Any, Dict[str, SimpleReport]] = {}

def _register_report(user_id: Any, report: SimpleReport) -> None:
    """Register a report in the in-memory registry."""
    user_reports = _reports_by_user.setdefault(user_id, {})
    user_reports[str(report.id)] = report


def create_report_from_file(
    *,
    filename: str,
    file_content: bytes,
    file_type: str,
    user_id: Any,
    db: Any,
    background_tasks: Optional[BackgroundTasks] = None,
) -> SimpleReport:
    """
    Create a report from an uploaded file.  Saves the file to disk,
    creates a database record, and schedules PDF preprocessing if applicable.

    :param filename: The original filename uploaded by the user.
    :param file_content: The raw bytes of the uploaded file.
    :param file_type: MIME type of the file (e.g., ``application/pdf``).
    :param user_id: Identifier for the user uploading the report.
    :param db: Database connection for persisting the report.
    :param background_tasks: Optional ``BackgroundTasks`` instance to
        schedule asynchronous preprocessing.
    :return: A :class:`SimpleReport` instance populated with metadata.
    """
    # Ensure the uploads directory exists
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # Generate a unique filename to avoid collisions
    report_id = str(uuid.uuid4())
    saved_filename = f"{report_id}_{filename}"
    file_path = os.path.join(uploads_dir, saved_filename)

    # Write the uploaded content to disk
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Save report to DATABASE (critical for pdf_cache foreign key constraint)
    report_crud = ReportCRUD()
    db_report = report_crud.create_report_with_blocks(
        report_id=report_id,
        title=filename,
        user_id=user_id,
        file_path=file_path,
        file_type=file_type,
        file_size=len(file_content),
        paragraphs=[],  # PDF reports start with no text blocks
        db=db,
    )

    # Schedule PDF preprocessing in background
    if background_tasks and file_type and file_type.lower().startswith("application/pdf"):
        background_tasks.add_task(
            cache_preprocess_pdf,
            report_id,
            file_path,
            file_type,
        )

    # Convert to SimpleReport for compatibility
    report = SimpleReport(report_id, file_path, file_type)
    report.title = filename
    report.file_size = len(file_content)
    report.created_at = db_report.created_at if db_report else datetime.utcnow()
    report.updated_at = db_report.updated_at if db_report else datetime.utcnow()
    report.blocks = db_report.blocks if db_report else []
    report.user_id = user_id

    # Also register in memory for backward compatibility
    _register_report(user_id, report)

    return report


def create_report_from_text(
    *,
    text_data: Any,
    user_id: Any,
    db: Any,
    background_tasks: Optional[BackgroundTasks] = None,
) -> SimpleReport:
    """
    Create a report from pasted text.  Saves the text content as a single
    block and registers the report in the in-memory store.

    :param text_data: An object with a ``text`` attribute containing the raw text.
    :param user_id: Identifier for the user uploading the report.
    :param db: Placeholder for a database session (unused in this stub).
    :param background_tasks: Optional unused parameter for parity.
    :return: A :class:`SimpleReport` instance populated with metadata.
    """
    report_id = str(uuid.uuid4())
    report = SimpleReport(report_id, file_path=None, file_type="text/plain")
    report.title = f"Text Report {report_id}"
    report.file_size = len(text_data.text.encode("utf-8"))
    now = datetime.utcnow()
    report.created_at = now
    report.updated_at = now
    report.blocks = [
        SimpleBlock(
            id=str(uuid.uuid4()),
            content=text_data.text,
            type="text",
            tags=[],
            order_index=0,
            created_at=now,
            updated_at=now,
        )
    ]
    report.user_id = user_id
    _register_report(user_id, report)
    return report


def get_user_reports(user_id: Any, db: Any) -> List[SimpleReport]:
    """Return all reports for a user from the in-memory registry."""
    return list(_reports_by_user.get(user_id, {}).values())


def get_report_by_id(report_id: str, user_id: Any, db: Any) -> Optional[SimpleReport]:
    """Retrieve a report by ID if it belongs to the specified user."""
    return _reports_by_user.get(user_id, {}).get(str(report_id))


def delete_report(report_id: str, user_id: Any, db: Any) -> Optional[str]:
    """
    Delete a report from the in-memory store and remove its file from disk.

    :param report_id: Identifier of the report to delete.
    :param user_id: User identifier to ensure ownership.
    :param db: Placeholder for a database session (unused).
    :return: The file path of the deleted report if removed.
    """
    user_reports = _reports_by_user.get(user_id)
    if not user_reports:
        return None
    report = user_reports.pop(str(report_id), None)
    if report and report.file_path and os.path.exists(report.file_path):
        try:
            os.remove(report.file_path)
        except Exception:
            pass
        return report.file_path
    return None


def get_page_info(report_id: str) -> list[dict[str, Any]]:
    """Return cached page metadata for a report.

    This is a thin wrapper around
    :func:`pdf_cache_service.get_page_info` that raises ``KeyError``
    when the report has not been preprocessed.
    """
    info = cache_get_page_info(report_id)
    if info is None:
        raise KeyError(f"Report {report_id} not preprocessed")
    return info


def get_page_image(report_id: str, page_number: int, scale: float = 1.0) -> bytes:
    """Return a cached page image or raise ``KeyError`` if missing.

    The caller is responsible for validating the ``scale`` range.
    """
    img = cache_get_page_image(report_id, page_number, scale)
    if img is None:
        raise KeyError(f"Page image not cached: {report_id} page {page_number}")
    return img


def get_page_words(report_id: str, page_number: int) -> dict[str, Any]:
    """Return cached word data for a page or raise ``KeyError`` if missing."""
    words = cache_get_page_words(report_id, page_number)
    if words is None:
        raise KeyError(f"Page words not cached: {report_id} page {page_number}")
    return words


class ReportService:
    """Compatibility shim exposing preprocessing and page access helpers.

    Some parts of the application may import ``report_service`` and
    expect an object with a ``preprocess_pdf`` attribute.  This class
    provides ``preprocess_pdf`` as a static method and delegates to
    :mod:`pdf_cache_service` for all caching operations.
    """

    # Static alias to pdf_cache_service.preprocess_pdf
    preprocess_pdf = staticmethod(cache_preprocess_pdf)
    # Static alias to report creation helper
    create_report = staticmethod(create_report)

    # Static aliases to in-memory CRUD helpers
    create_report_from_file = staticmethod(create_report_from_file)
    create_report_from_text = staticmethod(create_report_from_text)
    get_user_reports = staticmethod(get_user_reports)
    get_report_by_id = staticmethod(get_report_by_id)
    delete_report = staticmethod(delete_report)


# Export a singleton instance for convenience
report_service = ReportService()