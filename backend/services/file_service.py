import os
import uuid
from typing import Optional

from core.config import settings
from crud.file import file_crud
from fastapi import UploadFile
from models.file import FileUpload
from utils.file_utils import get_file_size, validate_file_type


class FileService:
    def upload_file(self, file: UploadFile, user_id: int, db) -> Optional[FileUpload]:
        # Validate file
        if not validate_file_type(file.filename):
            return None

        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)

        # Get file size
        file_size = get_file_size(file_path)

        # Save to database
        file_data = FileUpload(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type,
            user_id=user_id,
        )

        return file_crud.create_file_record(file_data, db)

    def get_user_files(self, user_id: int, db):
        return file_crud.get_user_files(user_id, db)

    def delete_file(self, file_id: int, user_id: int, db) -> bool:
        file_record = file_crud.get_file_by_id(file_id, user_id, db)
        if not file_record:
            return False

        # Delete physical file
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)

        # Delete database record
        return file_crud.delete_file(file_id, user_id, db)


file_service = FileService()
