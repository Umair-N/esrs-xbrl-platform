from typing import List
from uuid import UUID

from api.dep import get_current_user
from database.session import get_db
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    BackgroundTasks,
    Query,
)
from fastapi.responses import StreamingResponse, JSONResponse
from schemas.report import ReportBlockResponse, ReportResponse, TextUpload
from services.report_service import report_service
from utils.file_utils import validate_file_size, validate_file_type
from datetime import datetime
import json
from pathlib import Path
from io import BytesIO

# Import caching helpers from pdf_cache_service
from services.pdf_cache_service import (
    preprocess_pdf,
    get_page_info as cache_get_page_info,
    get_page_image as cache_get_page_image,
    get_page_words as cache_get_page_words,
)


router = APIRouter()


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
    background_tasks: BackgroundTasks,
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
            background_tasks=background_tasks,  # Pass background_tasks to service
        )

        # Background task scheduling now happens inside create_report_from_file

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


@router.get("/{report_id:uuid}", response_model=ReportResponse)
async def get_report(
    report_id: UUID, current_user=Depends(get_current_user), db=Depends(get_db)
):
    report = report_service.get_report_by_id(str(report_id), current_user.id, db)
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


@router.delete("/{report_id:uuid}")
async def delete_report(
    report_id: UUID, current_user=Depends(get_current_user), db=Depends(get_db)
):
    file_path = report_service.delete_report(str(report_id), current_user.id, db)
    from utils.file_utils import cleanup_file

    cleanup_file(file_path)
    return {"message": "Report deleted successfully"}


# ---------------------------------------------------------------------------
# PDF page endpoints
#
# These endpoints enable the frontend to display uploaded PDF reports
# with their original layout. They expose page dimensions, rendered
# page images and word-level bounding boxes using the caching service.

def _get_report_and_file(report_id: UUID, user_id: int, db):
    """Fetch a report by ID and return its file path and SQLAlchemy model.

    Raises a 404 error if the report does not exist or if it is
    missing a file_path (i.e., was created from pasted text).
    """
    report = report_service.get_report_by_id(str(report_id), user_id, db)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.file_path:
        raise HTTPException(status_code=400, detail="Report has no associated file")
    file_path = report.file_path
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="Report file not found on server")
    return report, file_path


@router.get("/{report_id:uuid}/pages_info")
async def get_pages_info(
    report_id: UUID,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Return basic information about each page of a PDF report.

    The response includes the page number, width, and height for ALL pages.
    Uses cached data where available, but reads PDF to get complete page list.
    """
    report, file_path = _get_report_and_file(report_id, current_user.id, db)

    # Pass file_path to get info for ALL pages, not just cached ones
    pages = cache_get_page_info(str(report.id), file_path=file_path)

    if not pages:
        raise HTTPException(status_code=404, detail="Report not preprocessed or no page data available")

    return {"pages": pages}


@router.get("/{report_id:uuid}/pages/{page_number}/image")
async def get_page_image(
    report_id: UUID,
    page_number: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    scale: float = Query(1.0, ge=0.5, le=2.0),
):
    """Return a JPEG image of the specified page in the PDF report.

    The image is retrieved from memory cache if available, otherwise
    regenerated on-demand from the PDF file.
    """
    report, file_path = _get_report_and_file(report_id, current_user.id, db)

    # Try to get image from cache or regenerate
    img_bytes = cache_get_page_image(str(report.id), page_number, scale, file_path=file_path)

    if not img_bytes:
        raise HTTPException(status_code=404, detail="Page image not available and could not be regenerated")

    return StreamingResponse(BytesIO(img_bytes), media_type="image/jpeg")


@router.get("/{report_id:uuid}/pages/{page_number}/words")
async def get_page_words(
    report_id: UUID,
    page_number: int,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Return word-level bounding boxes for a given PDF page.

    The response includes the page width and height and a list of words
    with their bounding boxes and local start/end indices. Data is
    retrieved from the database (persistent storage), or processed
    on-demand if not yet cached.
    """
    report, file_path = _get_report_and_file(report_id, current_user.id, db)

    # Pass file_path to enable on-demand processing for uncached pages
    data = cache_get_page_words(str(report.id), page_number, file_path=file_path)

    if not data:
        raise HTTPException(status_code=404, detail="Page words not available and could not be processed")

    return JSONResponse(content=data)
