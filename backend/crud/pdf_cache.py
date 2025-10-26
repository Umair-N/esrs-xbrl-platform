"""
CRUD operations for PDF cache entries.

Provides database operations for storing and retrieving preprocessed PDF page data.
"""

import logging
from uuid import UUID, uuid4
from typing import List, Optional, Dict, Any
from database.connection import db_manager
from models.pdf_cache import PDFCache
import json

logger = logging.getLogger(__name__)


def create_pdf_cache_entry(
    report_id: UUID,
    page_number: int,
    page_width: float,
    page_height: float,
    words: List[Dict[str, Any]],
    scale: float = 1.0,
    image: Optional[bytes] = None,
) -> Optional[PDFCache]:
    """
    Create a new PDF cache entry for a page.

    Args:
        report_id: UUID of the report
        page_number: Page number (1-indexed)
        page_width: Page width in points
        page_height: Page height in points
        words: List of word dictionaries with bbox, text, start_index, end_index
        scale: Scale factor (default 1.0)

    Returns:
        PDFCache object if successful, None otherwise
    """
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            # Wrap words array in a dict for JSONB storage
            words_json = json.dumps({"words": words})

            # Generate UUID explicitly for raw SQL insert
            entry_id = uuid4()

            cursor.execute(
                """
                INSERT INTO pdf_cache
                (id, report_id, page_number, page_width, page_height, words, scale, image)
                VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)
                ON CONFLICT (report_id, page_number, scale)
                DO UPDATE SET
                    page_width = EXCLUDED.page_width,
                    page_height = EXCLUDED.page_height,
                    words = EXCLUDED.words,
                    image = EXCLUDED.image,
                    updated_at = NOW()
                RETURNING id, report_id, page_number, page_width, page_height, words, scale, image, created_at, updated_at
                """,
                (str(entry_id), str(report_id), page_number, page_width, page_height, words_json, scale, image),
            )
            row = cursor.fetchone()
            conn.commit()

            if row:
                logger.info(f"Created/updated PDF cache entry for report {report_id}, page {page_number}")
                return _row_to_pdf_cache(row)
            return None

    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating PDF cache entry: {e}", exc_info=True)
        return None
    finally:
        db_manager.return_connection(conn)


def batch_create_pdf_cache_entries(
    entries: List[Dict[str, Any]],
) -> int:
    """
    Batch create multiple PDF cache entries in a single transaction.

    This is optimized for bulk inserts (e.g., during PDF preprocessing)
    to reduce connection pool pressure.

    Args:
        entries: List of dicts with keys: report_id, page_number, page_width,
                 page_height, words, scale, image

    Returns:
        Number of entries successfully created
    """
    if not entries:
        return 0

    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            # Build batch insert values
            values = []
            for entry in entries:
                entry_id = uuid4()
                words_json = json.dumps({"words": entry["words"]})
                values.append((
                    str(entry_id),
                    str(entry["report_id"]),
                    entry["page_number"],
                    entry["page_width"],
                    entry["page_height"],
                    words_json,
                    entry.get("scale", 1.0),
                    entry.get("image"),
                ))

            # Execute batch insert with executemany for better performance
            cursor.executemany(
                """
                INSERT INTO pdf_cache
                (id, report_id, page_number, page_width, page_height, words, scale, image)
                VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s)
                ON CONFLICT (report_id, page_number, scale)
                DO UPDATE SET
                    page_width = EXCLUDED.page_width,
                    page_height = EXCLUDED.page_height,
                    words = EXCLUDED.words,
                    image = EXCLUDED.image,
                    updated_at = NOW()
                """,
                values,
            )

            rows_affected = cursor.rowcount
            conn.commit()
            logger.info(f"Batch created/updated {rows_affected} PDF cache entries")
            return rows_affected

    except Exception as e:
        conn.rollback()
        logger.error(f"Error batch creating PDF cache entries: {e}", exc_info=True)
        return 0
    finally:
        db_manager.return_connection(conn)


def get_pdf_cache_entry(
    report_id: UUID,
    page_number: int,
    scale: float = 1.0,
) -> Optional[PDFCache]:
    """
    Retrieve a PDF cache entry for a specific page.

    Args:
        report_id: UUID of the report
        page_number: Page number (1-indexed)
        scale: Scale factor (default 1.0)

    Returns:
        PDFCache object if found, None otherwise
    """
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, report_id, page_number, page_width, page_height, words, scale, image, created_at, updated_at
                FROM pdf_cache
                WHERE report_id = %s AND page_number = %s AND scale = %s
                """,
                (str(report_id), page_number, scale),
            )
            row = cursor.fetchone()
            return _row_to_pdf_cache(row) if row else None

    except Exception as e:
        logger.error(f"Error retrieving PDF cache entry: {e}", exc_info=True)
        return None
    finally:
        db_manager.return_connection(conn)


def get_all_pages_for_report(
    report_id: UUID,
    scale: float = 1.0,
) -> List[PDFCache]:
    """
    Retrieve all cached pages for a report.

    Args:
        report_id: UUID of the report
        scale: Scale factor (default 1.0)

    Returns:
        List of PDFCache objects ordered by page_number
    """
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, report_id, page_number, page_width, page_height, words, scale, image, created_at, updated_at
                FROM pdf_cache
                WHERE report_id = %s AND scale = %s
                ORDER BY page_number ASC
                """,
                (str(report_id), scale),
            )
            rows = cursor.fetchall()
            return [_row_to_pdf_cache(row) for row in rows]

    except Exception as e:
        logger.error(f"Error retrieving PDF cache entries for report: {e}", exc_info=True)
        return []
    finally:
        db_manager.return_connection(conn)


def delete_pdf_cache_for_report(report_id: UUID) -> bool:
    """
    Delete all cached pages for a report.

    Args:
        report_id: UUID of the report

    Returns:
        True if successful, False otherwise
    """
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM pdf_cache WHERE report_id = %s",
                (str(report_id),),
            )
            deleted_count = cursor.rowcount
            conn.commit()
            logger.info(f"Deleted {deleted_count} PDF cache entries for report {report_id}")
            return True

    except Exception as e:
        conn.rollback()
        logger.error(f"Error deleting PDF cache entries: {e}", exc_info=True)
        return False
    finally:
        db_manager.return_connection(conn)


def get_page_info_for_report(report_id: UUID) -> List[Dict[str, Any]]:
    """
    Get page metadata (number, width, height) for all cached pages.

    Args:
        report_id: UUID of the report

    Returns:
        List of dicts with page_number, width, height
    """
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT page_number, page_width, page_height
                FROM pdf_cache
                WHERE report_id = %s
                ORDER BY page_number ASC
                """,
                (str(report_id),),
            )
            rows = cursor.fetchall()
            return [
                {
                    "page_number": row[0],
                    "width": row[1],
                    "height": row[2],
                }
                for row in rows
            ]

    except Exception as e:
        logger.error(f"Error retrieving page info: {e}", exc_info=True)
        return []
    finally:
        db_manager.return_connection(conn)


def _row_to_pdf_cache(row) -> PDFCache:
    """Convert database row to PDFCache object."""
    cache = PDFCache()
    cache.id = row[0]
    cache.report_id = row[1]
    cache.page_number = row[2]
    cache.page_width = row[3]
    cache.page_height = row[4]
    cache.words = row[5] if isinstance(row[5], dict) else {"words": []}
    cache.scale = row[6]
    cache.image = row[7] if len(row) > 7 else None  # Image bytes
    cache.created_at = row[8] if len(row) > 8 else None
    cache.updated_at = row[9] if len(row) > 9 else None
    return cache
