# schemas/taxonomy.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TaxonomyCreate(BaseModel):
    name: str  # display name

class TaxonomyOut(BaseModel):
    id: int
    name: str
    file_name: str
    enabled: bool
    created_at: datetime
    class Config:
        from_attributes = True

class UserTaxonomyOut(BaseModel):
    user_id: int
    taxonomy: TaxonomyOut | None
class TaxonomyRequestBody(BaseModel):
    taxonomy_ids: List[int] 