import os
import uuid
from datetime import datetime
from typing import List, Optional

from core.config import settings
from crud.report import report_crud
from models.report import Report, ReportBlock
from schemas.report import ReportCreate, TextUpload
from utils.file_utils import extract_text_from_file


class ReportService:
    def create_report_from_file(
        self, *, filename, file_content, file_type, user_id, db
    ) -> Optional[Report]:
        # Extract text
        extracted_text = extract_text_from_file(file_content, filename)
        if not extracted_text.strip():
            raise ValueError("No text could be extracted from the file")
        paragraphs = [p.strip() for p in extracted_text.split("\n\n") if p.strip()]

        # Save the uploaded file
        upload_id = str(uuid.uuid4())
        ext = os.path.splitext(filename)[1]
        safe_filename = f"{upload_id}{ext}"
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, safe_filename)
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Call CRUD to persist report+blocks
        return report_crud.create_report_with_blocks(
            report_id=upload_id,
            title=os.path.splitext(filename)[0],
            user_id=user_id,
            file_path=file_path,
            file_type=file_type,
            file_size=len(file_content),
            paragraphs=paragraphs,
            db=db,
        )

    def create_report_from_text(
        self, *, text_data: TextUpload, user_id: int, db
    ) -> Optional[Report]:
        paragraphs = [p.strip() for p in text_data.text.split("\n\n") if p.strip()]
        report_id = str(uuid.uuid4())
        return report_crud.create_report_with_blocks(
            report_id=report_id,
            title=text_data.title or "Pasted Report",
            user_id=user_id,
            file_path=None,
            file_type=None,
            file_size=None,
            paragraphs=paragraphs,
            db=db,
        )

    def get_user_reports(self, user_id, db) -> List[Report]:
        return report_crud.get_user_reports(user_id, db)

    def get_report_by_id(self, report_id, user_id, db) -> Optional[Report]:
        return report_crud.get_report_by_id(report_id, user_id, db)

    def delete_report(self, report_id, user_id, db) -> Optional[str]:
        """Returns file_path if there was an attached file, otherwise None"""
        return report_crud.delete_report(report_id, user_id, db)


report_service = ReportService()
