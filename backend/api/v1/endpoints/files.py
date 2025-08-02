from typing import List

from api.dep import get_current_user
from database.session import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from models.user import User
from schemas.file import FileUploadResponse
from services.file_service import file_service
from utils.file_utils import validate_file_size, validate_file_type

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    # Validate file type
    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed"
        )

    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)

    if not validate_file_size(file_size):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit",
        )

    # Reset file pointer
    await file.seek(0)

    # Upload file
    uploaded_file = file_service.upload_file(file, current_user.id, db)
    if not uploaded_file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to upload file"
        )

    return FileUploadResponse(
        id=uploaded_file.id,
        filename=uploaded_file.filename,
        original_filename=uploaded_file.original_filename,
        file_path=uploaded_file.file_path,
        file_size=uploaded_file.file_size,
        file_type=uploaded_file.file_type,
        created_at=uploaded_file.created_at,
    )


@router.get("/", response_model=List[FileUploadResponse])
async def get_user_files(
    current_user: User = Depends(get_current_user), db=Depends(get_db)
):
    files = file_service.get_user_files(current_user.id, db)
    return [
        FileUploadResponse(
            id=file.id,
            filename=file.filename,
            original_filename=file.original_filename,
            file_path=file.file_path,
            file_size=file.file_size,
            file_type=file.file_type,
            created_at=file.created_at,
        )
        for file in files
    ]


@router.delete("/{file_id}")
async def delete_file(
    file_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db)
):
    success = file_service.delete_file(file_id, current_user.id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return {"message": "File deleted successfully"}
