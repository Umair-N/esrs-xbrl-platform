from typing import List

from api.dep import get_current_user
from database.session import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from schemas.report import ReportBlockResponse, ReportCreate, ReportResponse, TextUpload
from services.report_service import report_service
from utils.file_utils import validate_file_size, validate_file_type

router = APIRouter()


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
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    try:
        report = report_service.create_report_from_file(
            filename=file.filename,
            file_content=content,
            file_type=file.content_type,
            user_id=current_user.id,
            db=db,
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
