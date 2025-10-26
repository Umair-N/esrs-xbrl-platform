"""
PDF caching and preprocessing service (Hybrid Architecture).

**HYBRID CACHING STRATEGY:**
- **Word data (critical)**: Stored in PostgreSQL database for persistence
- **Images (optional)**: Kept in memory cache for performance, regenerated on-demand

This ensures:
1. Word data survives backend restarts (essential for tagging)
2. Horizontal scaling works (all instances share database)
3. Images stay fast (memory cache) but can be regenerated
4. Database stays small (images not stored)

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
"""

from __future__ import annotations

import fitz  # type: ignore
import logging
from typing import Dict, Any, Optional
from uuid import UUID
from crud import pdf_cache as pdf_cache_crud

logger = logging.getLogger(__name__)


# In-memory cache for page IMAGES ONLY (words now in database)
_image_cache: Dict[str, Dict[str, bytes]] = {}  # report_id -> {(page_number, scale): bytes}


def _image_key(page_number: int, scale: float) -> str:
    return f"{page_number}-{scale}"


def preprocess_pdf(report_id: str, file_path: str, file_type: str, scale: float = 1.0, quick_mode: bool = False) -> None:
    """Preprocess a PDF by extracting page info, images and words.

    CACHING STRATEGY:
    - Processes ALL pages on first upload and saves to database
    - Word data + images saved to PostgreSQL (persistent)
    - Subsequent loads are INSTANT from database cache
    - SKIP preprocessing if data already exists in database

    This ensures "process once, load forever" behavior - after initial
    processing, all page loads are instant regardless of restarts/reloads.

    :param report_id: Unique identifier for the report.
    :param file_path: Path to the PDF file on disk.
    :param file_type: MIME type; only PDFs are processed.
    :param scale: Zoom factor (1.0 = 72 dpi).  Use lower values for
        faster rendering or higher for better quality.
    :param quick_mode: DEPRECATED - Now always processes all pages. Default False.
    """
    if not file_type.lower().startswith("application/pdf"):
        logger.info(f"Skipping non-PDF file for report {report_id}: {file_type}")
        return

    try:
        report_uuid = UUID(report_id)
    except ValueError:
        logger.error(f"Invalid report ID format: {report_id}")
        return

    # CHECK IF ALREADY CACHED: Skip preprocessing if data already exists in database
    # This prevents reprocessing on page reloads or when report is accessed again
    existing_pages = pdf_cache_crud.get_page_info_for_report(report_uuid)
    if existing_pages and len(existing_pages) > 0:
        logger.info(f"PDF already cached in database for report {report_id} ({len(existing_pages)} pages). Skipping preprocessing.")
        # Still initialize memory cache for images (will be regenerated on-demand if needed)
        if report_id not in _image_cache:
            _image_cache[report_id] = {}
        return

    logger.info(f"Starting PDF preprocessing for report {report_id} - processing ALL pages")

    try:
        doc = fitz.open(file_path)
        total_pages = doc.page_count
        logger.info(f"Successfully opened PDF with {total_pages} pages for report {report_id}")
    except Exception as e:
        logger.error(f"Failed to open PDF file for report {report_id}: {e}", exc_info=True)
        return

    # Initialize image cache for this report
    if report_id not in _image_cache:
        _image_cache[report_id] = {}

    # Collect all page data for batch insert
    batch_entries = []
    pages_to_process = total_pages

    # Process pages and collect data
    for i in range(pages_to_process):
        page = doc.load_page(i)
        rect = page.rect
        page_number = i + 1

        # 1. Extract words and render image
        try:
            words = page.get_text("words")
            result_words = []

            # Calculate cumulative character indices across the page
            char_offset = 0
            for w in words:
                x0, y0, x1, y1, text, *_ = w
                text_length = len(text)
                result_words.append(
                    {
                        "bbox": [x0, y0, x1, y1],
                        "text": text,
                        "start_index": char_offset,
                        "end_index": char_offset + text_length,
                    }
                )
                # Move offset forward by text length + 1 space separator
                char_offset += text_length + 1

            # 2. Render page image as JPEG
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            img_bytes = pix.tobytes("jpeg")

            # 3. Collect for batch insert
            batch_entries.append({
                "report_id": report_uuid,
                "page_number": page_number,
                "page_width": rect.width,
                "page_height": rect.height,
                "words": result_words,
                "scale": scale,
                "image": img_bytes,
            })

            # Also cache image in memory for faster access during this session
            key = _image_key(page_number, scale)
            _image_cache[report_id][key] = img_bytes
            logger.debug(f"Prepared page {page_number} for batch insert")

        except Exception as e:
            logger.error(f"Failed to process page {page_number} for report {report_id}: {e}")

    doc.close()

    # Batch insert all pages in a single transaction to minimize connection usage
    if batch_entries:
        pages_processed = pdf_cache_crud.batch_create_pdf_cache_entries(batch_entries)
        logger.info(f"✅ Preprocessing complete for report {report_id}: {pages_processed}/{total_pages} pages saved to database. All future loads will be INSTANT!")
    else:
        logger.warning(f"No pages were successfully processed for report {report_id}")


def get_page_info(report_id: str, file_path: Optional[str] = None) -> Optional[list[dict[str, Any]]]:
    """
    Return page metadata for ALL pages in a PDF report.

    Uses cached data from database where available, but if file_path is provided
    and some pages are not cached (e.g., in quick mode), it will read the PDF
    to get total page count and dimensions for uncached pages.

    Returns list of {page_number, width, height} for ALL pages or None if not found.
    """
    try:
        report_uuid = UUID(report_id)
        cached_pages = pdf_cache_crud.get_page_info_for_report(report_uuid)

        # If we have cached pages and a file path, check if we need to add uncached pages
        if file_path:
            try:
                doc = fitz.open(file_path)
                total_pages = doc.page_count

                # Create a dict of cached pages for quick lookup
                cached_dict = {p['page_number']: p for p in (cached_pages or [])}

                # Build complete page list
                all_pages = []
                for page_num in range(1, total_pages + 1):
                    if page_num in cached_dict:
                        # Use cached dimensions
                        all_pages.append(cached_dict[page_num])
                    else:
                        # Get dimensions from PDF for uncached pages
                        page = doc.load_page(page_num - 1)
                        rect = page.rect
                        all_pages.append({
                            'page_number': page_num,
                            'page_width': rect.width,
                            'page_height': rect.height,
                        })

                doc.close()
                logger.debug(f"Returned info for {len(all_pages)} pages ({len(cached_dict)} cached, {len(all_pages) - len(cached_dict)} from PDF)")
                return all_pages

            except Exception as e:
                logger.error(f"Failed to read PDF for page info: {e}")
                # Fall back to cached pages only
                return cached_pages if cached_pages else None

        # No file path provided, return only cached pages
        return cached_pages if cached_pages else None

    except ValueError:
        logger.error(f"Invalid report ID format: {report_id}")
        return None
    except Exception as e:
        logger.error(f"Error fetching page info from database: {e}")
        return None


def get_page_image(report_id: str, page_number: int, scale: float, file_path: Optional[str] = None) -> Optional[bytes]:
    """
    Return a cached page image from DATABASE or MEMORY, or regenerate on-demand if missing.

    Priority: Memory cache > Database cache > Regenerate from PDF

    :param report_id: Report UUID as string
    :param page_number: Page number (1-indexed)
    :param scale: Scale factor
    :param file_path: Optional path to PDF file for regeneration
    :return: JPEG bytes or None
    """
    try:
        report_uuid = UUID(report_id)
    except ValueError:
        logger.error(f"Invalid report ID format: {report_id}")
        return None

    # 1. Check memory cache first (fastest)
    images = _image_cache.get(report_id)
    if images:
        key = _image_key(page_number, scale)
        cached = images.get(key)
        if cached:
            logger.debug(f"Image MEMORY cache HIT for report {report_id}, page {page_number}")
            return cached

    # 2. Check database cache (persistent, survives restarts)
    cache_entry = pdf_cache_crud.get_pdf_cache_entry(report_uuid, page_number, scale)
    if cache_entry and cache_entry.image:
        logger.debug(f"Image DATABASE cache HIT for report {report_id}, page {page_number}")
        # Also store in memory for faster next access
        if report_id not in _image_cache:
            _image_cache[report_id] = {}
        _image_cache[report_id][_image_key(page_number, scale)] = cache_entry.image
        return cache_entry.image

    logger.debug(f"Image cache MISS (both memory and database) for report {report_id}, page {page_number}")

    # 3. Regenerate from PDF if file_path provided
    if file_path:
        try:
            logger.info(f"Regenerating image for report {report_id}, page {page_number}")
            doc = fitz.open(file_path)
            if page_number < 1 or page_number > doc.page_count:
                logger.error(f"Invalid page number {page_number} for report {report_id}")
                doc.close()
                return None

            page = doc.load_page(page_number - 1)  # 0-indexed
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            img_bytes = pix.tobytes("jpeg")
            doc.close()

            # Cache in memory for this session
            if report_id not in _image_cache:
                _image_cache[report_id] = {}
            _image_cache[report_id][_image_key(page_number, scale)] = img_bytes

            return img_bytes

        except Exception as e:
            logger.error(f"Failed to regenerate image for page {page_number}: {e}")
            return None

    return None


def get_page_words(report_id: str, page_number: int, file_path: Optional[str] = None) -> Optional[dict[str, Any]]:
    """
    Return word data for a page from DATABASE, or process on-demand if not cached.

    ON-DEMAND PROCESSING:
    If the page is not in the database (e.g., beyond first 3 pages in quick mode),
    and file_path is provided, this function will process that page immediately
    and save it to the database before returning.

    :param report_id: Report UUID as string
    :param page_number: Page number (1-indexed)
    :param file_path: Optional path to PDF file for on-demand processing
    :return: Dict with {words: [...], page_width: N, page_height: M} or None
    """
    try:
        report_uuid = UUID(report_id)
        cache_entry = pdf_cache_crud.get_pdf_cache_entry(report_uuid, page_number)

        if cache_entry:
            logger.debug(f"Word data found in database for report {report_id}, page {page_number}")
            return cache_entry.to_dict()

        logger.debug(f"No word data in database for report {report_id}, page {page_number}")

        # Page not cached - try on-demand processing if file_path provided
        if file_path:
            logger.info(f"Triggering on-demand processing for report {report_id}, page {page_number}")
            from services.pdf_on_demand import process_single_page
            result = process_single_page(report_id, file_path, page_number)
            if result:
                logger.info(f"Successfully processed page {page_number} on-demand")
                return result
            else:
                logger.error(f"On-demand processing failed for page {page_number}")
                return None

        return None

    except ValueError:
        logger.error(f"Invalid report ID format: {report_id}")
        return None
    except Exception as e:
        logger.error(f"Error fetching word data from database: {e}", exc_info=True)
        return None