"""
PDF caching and preprocessing service.

This module provides functions to preload PDF pages, cache rasterised
images and word bounding boxes, and serve them efficiently.  It does
not depend on the existing ReportService or database models, so it can
be integrated into any FastAPI application without interfering with
existing endpoints.

Usage:
    from services.pdf_cache_service import (
        preprocess_pdf,
        get_page_info,
        get_page_image,
        get_page_words,
    )

    # Schedule preprocessing after uploading a PDF
    background_tasks.add_task(preprocess_pdf, report_id, file_path, file_type, scale=1.0)

    # In your API endpoints
    pages = get_page_info(report_id)
    img_bytes = get_page_image(report_id, page_number, scale)
    words_data = get_page_words(report_id, page_number)

The preprocessing function caches all pages at the specified scale.
If a page has already been cached it will be skipped.  The caches
are stored in memory; for persistence across process restarts consider
using an external cache such as Redis or writing the data to disk.

Reference: Processing large PDFs one page at a time and tuning
resolution improves performance【208437848823784†L395-L403】.
"""

from __future__ import annotations

import fitz  # type: ignore
from typing import Dict, Any, Optional


# In-memory caches for PDF metadata and page content
_info_cache: Dict[str, list[dict[str, Any]]] = {}
_image_cache: Dict[str, Dict[str, bytes]] = {}  # report_id -> {(page_number, scale): bytes}
_words_cache: Dict[str, Dict[int, dict[str, Any]]] = {}  # report_id -> {page_number: data}


def _image_key(page_number: int, scale: float) -> str:
    return f"{page_number}-{scale}"


def preprocess_pdf(report_id: str, file_path: str, file_type: str, scale: float = 1.0) -> None:
    """Preprocess a PDF by extracting page info, images and words.

    :param report_id: Unique identifier for the report.
    :param file_path: Path to the PDF file on disk.
    :param file_type: MIME type; only PDFs are processed.
    :param scale: Zoom factor (1.0 = 72 dpi).  Use lower values for
        faster rendering or higher for better quality.
    """
    if not file_type.lower().startswith("application/pdf"):
        return
    try:
        doc = fitz.open(file_path)
    except Exception:
        return
    # Initialise caches for this report
    if report_id not in _info_cache:
        _info_cache[report_id] = []
    if report_id not in _image_cache:
        _image_cache[report_id] = {}
    if report_id not in _words_cache:
        _words_cache[report_id] = {}
    # Extract page info
    if not _info_cache[report_id]:
        for i in range(doc.page_count):
            page = doc.load_page(i)
            rect = page.rect
            _info_cache[report_id].append(
                {
                    "page_number": i + 1,
                    "width": rect.width,
                    "height": rect.height,
                }
            )
    # Process pages
    for i in range(doc.page_count):
        key = _image_key(i + 1, scale)
        if key not in _image_cache[report_id]:
            page = doc.load_page(i)
            mat = fitz.Matrix(scale, scale)
            try:
                pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
                _image_cache[report_id][key] = pix.tobytes("jpeg")
            except Exception:
                pass
        if i + 1 not in _words_cache[report_id]:
            page = doc.load_page(i)
            try:
                words = page.get_text("words")
                result_words = []
                for w in words:
                    x0, y0, x1, y1, text, *_ = w
                    result_words.append(
                        {
                            "bbox": [x0, y0, x1, y1],
                            "text": text,
                            # character indices are not provided here
                            "start_index": 0,
                            "end_index": len(text),
                        }
                    )
                rect = page.rect
                _words_cache[report_id][i + 1] = {
                    "words": result_words,
                    "page_width": rect.width,
                    "page_height": rect.height,
                }
            except Exception:
                pass
    doc.close()


def get_page_info(report_id: str) -> Optional[list[dict[str, Any]]]:
    """Return cached page metadata for a report or None if missing."""
    return _info_cache.get(report_id)


def get_page_image(report_id: str, page_number: int, scale: float) -> Optional[bytes]:
    """Return a cached page image or None if not available."""
    images = _image_cache.get(report_id)
    if not images:
        return None
    return images.get(_image_key(page_number, scale))


def get_page_words(report_id: str, page_number: int) -> Optional[dict[str, Any]]:
    """Return cached word data or None if not available."""
    words = _words_cache.get(report_id)
    if not words:
        return None
    return words.get(page_number)