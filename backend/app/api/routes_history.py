from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from ..core.database import get_db
from ..core.config import settings
from ..models.result import DetectionResult
from ..schemas.result import HistoryPage, DetectionOutput

router = APIRouter()

@router.get("/history", response_model=HistoryPage)
def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    q: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    min_count: int | None = Query(None, ge=0),
    max_count: int | None = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    filters = []
    if q:
        filters.append(DetectionResult.original_filename.ilike(f"%{q}%"))
    if date_from:
        filters.append(DetectionResult.created_at >= date_from)
    if date_to:
        filters.append(DetectionResult.created_at <= date_to)
    if min_count is not None:
        filters.append(DetectionResult.people_count >= min_count)
    if max_count is not None:
        filters.append(DetectionResult.people_count <= max_count)

    where = and_(*filters) if filters else None

    # total = db.scalar(select(func.count()).select_from(DetectionResult).where(where) if where else select(func.count()).select_from(DetectionResult))
    # stmt = select(DetectionResult).where(where) if where else select(DetectionResult)
    # stmt = stmt.order_by(DetectionResult.created_at.desc()).limit(page_size).offset((page-1)*page_size)
    
    # build total query
    stmt_total = select(func.count()).select_from(DetectionResult)
    if where is not None:
        stmt_total = stmt_total.where(where)
    total = db.scalar(stmt_total)

    # build main query
    stmt = select(DetectionResult)
    if where is not None:
        stmt = stmt.where(where)
    stmt = stmt.order_by(DetectionResult.created_at.desc()) \
               .limit(page_size) \
               .offset((page - 1) * page_size)
    
    rows: List[DetectionResult] = db.execute(stmt).scalars().all()

    items = []
    for r in rows:
        filename = r.processed_path.split("/")[-1]
        processed_url = f"{settings.BASE_URL}/static/{filename}"
        items.append(DetectionOutput(
            id=r.id, created_at=r.created_at, original_filename=r.original_filename,
            processed_url=processed_url, people_count=r.people_count
        ))

    return HistoryPage(total=total or 0, page=page, page_size=page_size, items=items)
