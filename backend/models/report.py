from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from models.base import BaseModel


@dataclass
class ReportBlock(BaseModel):
    report_id: str = ""
    content: str = ""
    type: str = ""
    tags: List[str] = None
    order_index: int = 0


@dataclass
class Report(BaseModel):
    title: str = ""
    user_id: int = 0
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    blocks: List[ReportBlock] = None
