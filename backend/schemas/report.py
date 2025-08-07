from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ReportBlockCreate(BaseModel):
    content: str
    type: str
    tags: List[str] = []


class ReportBlockResponse(BaseModel):
    id: str
    content: str
    type: str
    tags: List[str] = []
    order_index: int
    created_at: Optional[datetime] = None  # Made optional to avoid validation error


class ReportCreate(BaseModel):
    title: str
    blocks: List[ReportBlockCreate] = []


class ReportResponse(BaseModel):
    id: str
    title: str
    file_path: Optional[str]
    file_size: Optional[int]
    file_type: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    blocks: List[ReportBlockResponse] = []


class TextUpload(BaseModel):
    text: str
    title: Optional[str] = "Pasted Report"
