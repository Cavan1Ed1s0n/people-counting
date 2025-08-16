from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DetectionOutput(BaseModel):
    id: int
    created_at: datetime
    original_filename: str
    processed_url: str
    people_count: int

class HistoryQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    q: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_count: Optional[int] = Field(None, ge=0)
    max_count: Optional[int] = Field(None, ge=0)

class HistoryPage(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[DetectionOutput]
