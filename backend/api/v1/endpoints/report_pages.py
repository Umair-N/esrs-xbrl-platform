"""
Additional endpoints for PDF page metadata and content.

These endpoints supplement the existing report API by providing
lightweight page metadata, rasterised page images at a configurable
scale, and word bounding boxes for each page.  They do not
overwrite any existing report routes (e.g., upload) and can be
registered alongside the existing endpoints.

To enable these endpoints, import the router in ``api/v1/api.py`` and
include it with an appropriate prefix:

    from api.v1.endpoints.report_pages import router as report_pages_router
    api_router.include_router(report_pages_router, prefix="/reports")

This will expose the following routes:
    GET /reports/{report_id}/pages_info
    GET /reports/{report_id}/pages/{page_number}/image?scale=1.0
    GET /reports/{report_id}/pages/{page_number}/words

Before requesting images or words, ensure that the report has been
preprocessed using :func:`preprocess_pdf` from
``services.pdf_cache_service``.  Otherwise a 404 is returned.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
import io

from services.pdf_cache_service import (
    get_page_info,
    get_page_image,
    get_page_words,
)

router = APIRouter()


@router.get("/{report_id}/pages_info")
async def pages_info(report_id: str):
    info = get_page_info(report_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Report not preprocessed")
    return {"pages": info}


@router.get("/{report_id}/pages/{page_number}/image")
async def page_image(
    report_id: str,
    page_number: int,
    scale: float = Query(1.0, ge=0.5, le=2.0),
):
    img = get_page_image(report_id, page_number, scale)
    if img is None:
        raise HTTPException(status_code=404, detail="Page image not cached")
    return StreamingResponse(io.BytesIO(img), media_type="image/jpeg")


@router.get("/{report_id}/pages/{page_number}/words")
async def page_words(report_id: str, page_number: int):
    data = get_page_words(report_id, page_number)
    if data is None:
        raise HTTPException(status_code=404, detail="Page words not cached")
    return JSONResponse(content=data)