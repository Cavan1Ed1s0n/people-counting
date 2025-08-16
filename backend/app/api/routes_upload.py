import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import cv2
import numpy as np
from pathlib import Path

from ..core.database import get_db
from ..core.config import settings
from ..models.result import DetectionResult
from ..schemas.result import DetectionOutput
from ..services.storage import ensure_storage
from ..services.detection import detect_people

router = APIRouter()

@router.post("/upload", response_model=DetectionOutput)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status_code=400, detail="Unsupported image type")

    image_bytes = await file.read()

    img, people_count = detect_people(image_bytes)

    out_dir: Path = ensure_storage()
    ext = ".jpg"
    out_name = f"{uuid.uuid4().hex}{ext}"
    out_path = out_dir / out_name
    cv2.imwrite(str(out_path), img)

    rec = DetectionResult(
        original_filename=file.filename or "",
        processed_path=str(out_path),
        people_count=people_count,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    # static route exposes /static/<filename>
    public_url = f"{settings.BASE_URL}/static/{out_name}"

    return DetectionOutput(
        id=rec.id,
        created_at=rec.created_at,
        original_filename=rec.original_filename,
        processed_url=public_url,
        people_count=rec.people_count,
    )
