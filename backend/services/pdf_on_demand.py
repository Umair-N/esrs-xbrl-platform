"""
On-demand PDF page processing.

When a page is requested but not yet cached, this module processes it
immediately and saves to the database. This enables fast initial load
by deferring processing of pages beyond the first 3.
"""

import fitz  # type: ignore
import logging
from uuid import UUID
from typing import Optional, Dict, Any
from crud import pdf_cache as pdf_cache_crud

logger = logging.getLogger(__name__)


def process_single_page(
    report_id: str,
    file_path: str,
    page_number: int,
    scale: float = 1.0,
) -> Optional[Dict[str, Any]]:
    """
    Process a single PDF page on-demand if not already cached.

    This function is called when the frontend requests a page that
    hasn't been preprocessed yet. It extracts word data and saves
    to the database, then returns the page data immediately.

    :param report_id: UUID of the report
    :param file_path: Path to PDF file on disk
    :param page_number: Page number to process (1-indexed)
    :param scale: Scale factor for rendering
    :return: Dict with page_width, page_height, words, or None on error
    """
    try:
        report_uuid = UUID(report_id)
    except ValueError:
        logger.error(f"Invalid report ID format: {report_id}")
        return None

    # Check if page already exists in database
    existing = pdf_cache_crud.get_pdf_cache_entry(report_uuid, page_number, scale)
    if existing:
        logger.debug(f"Page {page_number} already cached for report {report_id}")
        return existing.to_dict()

    # Process the page
    logger.info(f"Processing page {page_number} on-demand for report {report_id}")

    try:
        doc = fitz.open(file_path)

        if page_number < 1 or page_number > doc.page_count:
            logger.error(f"Invalid page number {page_number} for report {report_id} (total: {doc.page_count})")
            doc.close()
            return None

        # Load the specific page (0-indexed)
        page = doc.load_page(page_number - 1)
        rect = page.rect

        # Extract words with bounding boxes
        words = page.get_text("words")
        result_words = []

        # Calculate cumulative character indices
        char_offset = 0
        for w in words:
            x0, y0, x1, y1, text, *_ = w
            text_length = len(text)
            result_words.append({
                "bbox": [x0, y0, x1, y1],
                "text": text,
                "start_index": char_offset,
                "end_index": char_offset + text_length,
            })
            char_offset += text_length + 1

        # Render page image
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img_bytes = pix.tobytes("jpeg")

        doc.close()

        # Save words + image to database
        cache_entry = pdf_cache_crud.create_pdf_cache_entry(
            report_id=report_uuid,
            page_number=page_number,
            page_width=rect.width,
            page_height=rect.height,
            words=result_words,
            scale=scale,
            image=img_bytes,  # Save image to database!
        )

        if cache_entry:
            logger.info(f"Successfully processed and cached page {page_number} for report {report_id}")
            return cache_entry.to_dict()
        else:
            logger.error(f"Failed to cache page {page_number} for report {report_id}")
            return None

    except Exception as e:
        logger.error(f"Error processing page {page_number} for report {report_id}: {e}", exc_info=True)
        return None
