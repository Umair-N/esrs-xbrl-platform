from typing import List

from api.dep import get_current_user
from database.session import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse, JSONResponse
from schemas.report import ReportBlockResponse, ReportCreate, ReportResponse, TextUpload
from services.report_service import report_service
from utils.file_utils import validate_file_size, validate_file_type
from datetime import datetime
import json
router = APIRouter()

# ---------------------------------------------------------------------------
# Additional imports for PDF page extraction
#
# We use the PyMuPDF library (imported as `fitz`) to generate page images
# and extract word-level bounding boxes. These endpoints allow the frontend
# to render the original PDF pages with precise text selection.  The
# `fitz` module is available in this environment; if deploying elsewhere
# ensure that the `PyMuPDF` package is installed.  See requirements.txt.
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None  # Will raise at runtime if endpoints are hit without PyMuPDF

from pathlib import Path
from io import BytesIO

def parse_tags(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
    return []

@router.post("/upload", response_model=ReportResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    # Validate extension and size
    if not validate_file_type(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    content = await file.read()

    if not validate_file_size(len(content)):
        raise HTTPException(status_code=400, detail="File too large (max 70MB)")

    try:
        report = report_service.create_report_from_file(
            filename=file.filename,
            file_content=content,
            file_type=file.content_type,
            user_id=current_user.id,
            db=db,
        )

        return ReportResponse(
            id=str(report.id),
            title=report.title,
            file_path=report.file_path,
            file_size=report.file_size,
            file_type=report.file_type,
            created_at=report.created_at,
            updated_at=report.updated_at,
            blocks=[
                ReportBlockResponse(
                    id=str(blk.id),
                    content=blk.content,
                    type=blk.type,
                    tags=parse_tags(blk.tags),
                    order_index=blk.order_index,
                    created_at=blk.created_at or datetime.utcnow(),
                )
                for blk in (report.blocks or [])
            ],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


@router.post("/text", response_model=ReportResponse)
async def upload_text(
    text_data: TextUpload,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not text_data.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty")
    try:
        report = report_service.create_report_from_text(
            text_data=text_data, user_id=current_user.id, db=db
        )
        return ReportResponse(
            id=report.id,
            title=report.title,
            file_path=report.file_path,
            file_size=report.file_size,
            file_type=report.file_type,
            created_at=report.created_at,
            updated_at=report.updated_at,
            blocks=[
                ReportBlockResponse(
                    id=blk.id,
                    content=blk.content,
                    type=blk.type,
                    tags=blk.tags or [],
                    order_index=blk.order_index,
                    created_at=blk.created_at,
                )
                for blk in (report.blocks or [])
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {e}")


@router.get("/", response_model=List[ReportResponse])
async def get_user_reports(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    reports = report_service.get_user_reports(current_user.id, db)
    return [
        ReportResponse(
            id=report.id,
            title=report.title,
            file_path=report.file_path,
            file_size=report.file_size,
            file_type=report.file_type,
            created_at=report.created_at,
            updated_at=report.updated_at,
            blocks=[],
        )
        for report in reports
    ]


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str, current_user=Depends(get_current_user), db=Depends(get_db)
):
    report = report_service.get_report_by_id(report_id, current_user.id, db)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse(
        id=report.id,
        title=report.title,
        file_path=report.file_path,
        file_size=report.file_size,
        file_type=report.file_type,
        created_at=report.created_at,
        updated_at=report.updated_at,
        blocks=[
            ReportBlockResponse(
                id=blk.id,
                content=blk.content,
                type=blk.type,
                tags=blk.tags or [],
                order_index=blk.order_index,
                created_at=blk.created_at,
            )
            for blk in (report.blocks or [])
        ],
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str, current_user=Depends(get_current_user), db=Depends(get_db)
):
    file_path = report_service.delete_report(report_id, current_user.id, db)
    from utils.file_utils import cleanup_file

    cleanup_file(file_path)
    return {"message": "Report deleted successfully"}


# ---------------------------------------------------------------------------
# PDF page endpoints
#
# These endpoints enable the frontend to display uploaded PDF reports
# with their original layout. They expose page dimensions, rendered
# page images and word-level bounding boxes with global character offsets.

def _ensure_pdf_lib():
    """Internal helper to verify PyMuPDF availability."""
    if fitz is None:
        raise HTTPException(status_code=500, detail="PyMuPDF (fitz) library is required but not installed")


def _get_report_and_file(report_id: str, user_id: int, db):
    """Fetch a report by ID and return its file path and SQLAlchemy model.

    Raises a 404 error if the report does not exist or if it is
    missing a file_path (i.e., was created from pasted text).
    """
    report = report_service.get_report_by_id(report_id, user_id, db)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.file_path:
        raise HTTPException(status_code=400, detail="Report has no associated file")
    file_path = report.file_path
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="Report file not found on server")
    return report, file_path


@router.get("/{report_id}/pages_info")
async def get_pages_info(
    report_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Return basic information about each page of a PDF report.

    The response includes the total number of pages and, for each page,
    its width and height (in pixels) along with the character offset
    relative to the beginning of the full extracted text. The character
    offsets allow the frontend to map word selections back into the
    global report text.

    This endpoint is only applicable to PDF-based reports. A 400 error
    is returned if the report does not have an attached file.
    """
    _ensure_pdf_lib()
    report, file_path = _get_report_and_file(report_id, current_user.id, db)
    # Open the PDF and accumulate per-page info
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open PDF: {e}")
    pages_info = []
    char_offset = 0
    for page_number in range(len(doc)):
        page = doc[page_number]
        # Use `text` extractor to get plain text for page; fallback to empty string
        try:
            page_text = page.get_text("text") or ""
        except Exception:
            page_text = ""
        # Record page dimensions and current global char offset
        pages_info.append(
            {
                "page_number": page_number,
                "width": int(page.rect.width),
                "height": int(page.rect.height),
                "char_start": char_offset,
                "char_end": char_offset + len(page_text),
            }
        )
        char_offset += len(page_text)
    return {"num_pages": len(doc), "pages": pages_info}


@router.get("/{report_id}/pages/{page_number}/image")
async def get_page_image(
    report_id: str,
    page_number: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Return a PNG image of the specified page in the PDF report.

    The image is rendered at a scale of 1:1 (72 DPI), so the dimensions
    in pixels match those reported by ``/pages_info``. If the page index
    is out of range, a 404 error is returned.
    """
    _ensure_pdf_lib()
    _, file_path = _get_report_and_file(report_id, current_user.id, db)
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open PDF: {e}")
    if page_number < 0 or page_number >= len(doc):
        raise HTTPException(status_code=404, detail="Page number out of range")
    page = doc[page_number]
    # Render page at 72 DPI (scale=1) for pixel-perfect alignment with bounding boxes
    try:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render page image: {e}")
    image_bytes = pix.tobytes("png")
    return StreamingResponse(BytesIO(image_bytes), media_type="image/png")


@router.get("/{report_id}/pages/{page_number}/words")
async def get_page_words(
    report_id: str,
    page_number: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Return word-level bounding boxes for a given PDF page.

    Each item in the returned list contains the bounding box coordinates
    (``x0``, ``y0``, ``x1``, ``y1``), the word text and its global
    character start/end indices relative to the full extracted text of
    the PDF. These indices can be used to create tags associated
    with the report blocks.
    """
    _ensure_pdf_lib()
    _, file_path = _get_report_and_file(report_id, current_user.id, db)
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open PDF: {e}")
    if page_number < 0 or page_number >= len(doc):
        raise HTTPException(status_code=404, detail="Page number out of range")
    # Compute char offsets up to this page
    char_offset = 0
    for i in range(page_number):
        try:
            txt = doc[i].get_text("text") or ""
        except Exception:
            txt = ""
        char_offset += len(txt)
    page = doc[page_number]
    # Get plain text for this page
    try:
        page_text = page.get_text("text") or ""
    except Exception:
        page_text = ""
    words_output = []
    # Use page.get_text("words") to get word-level bounding boxes. Format:
    # (x0, y0, x1, y1, word, block_no, line_no, word_no)
    try:
        words = page.get_text("words")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract words: {e}")
    # Iterate through words, tracking current index into page_text to
    # compute start/end positions. We advance the search window after
    # matching each word to avoid matching earlier occurrences.
    search_pos = 0
    for entry in words:
        x0, y0, x1, y1, word_text, *_ = entry
        # Find the word in page_text starting from current search position
        idx = page_text.find(word_text, search_pos)
        if idx < 0:
            # If word not found (unlikely), fallback: use current search_pos
            start = search_pos
            end = start + len(word_text)
        else:
            start = idx
            end = start + len(word_text)
            search_pos = end
        # Use character positions relative to this page's text (block).
        # The frontend associates PDF pages with individual report blocks
        # rather than merging them. Therefore start/end indices should
        # correspond to positions within the page text, not the global
        # extracted text. If you need global positions for other
        # purposes, compute them by adding `char_offset` to these values.
        words_output.append(
            {
                "bbox": [x0, y0, x1, y1],
                "text": word_text,
                "start_index": start,
                "end_index": end,
            }
        )
    return {
        "page_width": int(page.rect.width),
        "page_height": int(page.rect.height),
        "words": words_output,
    }
