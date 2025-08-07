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
        self, 
        filename: str, 
        file_content: bytes, 
        file_type: str, 
        user_id: int, 
        db
    ) -> Report:
        """Create report from uploaded file"""
        # Extract text from file
        try:
            extracted_text = extract_text_from_file(file_content, filename)
        except Exception as e:
            raise ValueError(f"Could not extract text from file: {str(e)}")
            
        if not extracted_text.strip():
            raise ValueError("No text could be extracted from the file")
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in extracted_text.split("\n\n") if p.strip()]
        
        if not paragraphs:
            raise ValueError("No content found in file")

        # Save file to disk
        file_id = str(uuid.uuid4())
        report_id = str(uuid.uuid4())
        ext = os.path.splitext(filename)[1].lower()
        safe_filename = f"{file_id}{ext}"
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, safe_filename)
        
        # Ensure directory exists
        os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
        
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
        except Exception as e:
            raise ValueError(f"Could not save file: {str(e)}")
        # Create report with blocks
        return report_crud.create_report_with_blocks(
            title=os.path.splitext(filename)[0] or "Uploaded Report",
            user_id=user_id,
            paragraphs=paragraphs,
            file_path=file_path,
            file_type=file_type,
            file_size=len(file_content),
            db=db,
            report_id=report_id
        )

    def create_report_from_text(
        self, 
        text_data: TextUpload, 
        user_id: int, 
        db
    ) -> Report:
        """Create report from text input"""
        if not text_data.text.strip():
            raise ValueError("Text content cannot be empty")
            
        # Split into paragraphs
        paragraphs = [p.strip() for p in text_data.text.split("\n\n") if p.strip()]
        
        if not paragraphs:
            raise ValueError("No content found in text")
        
        return report_crud.create_report_with_blocks(
            title=text_data.title or "Text Report",
            user_id=user_id,
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
