from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.base import BaseModel


@dataclass
class FileUpload(BaseModel):
    filename: str = ""
    original_filename: str = ""
    file_path: str = ""
    file_size: int = 0
    file_type: str = ""
    user_id: int = 0
