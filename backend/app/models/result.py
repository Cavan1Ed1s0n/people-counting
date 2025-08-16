from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from ..core.database import Base

class DetectionResult(Base):
    __tablename__ = "detection_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    original_filename: Mapped[str] = mapped_column(String(512))
    processed_path: Mapped[str] = mapped_column(String(1024))
    people_count: Mapped[int] = mapped_column(Integer)