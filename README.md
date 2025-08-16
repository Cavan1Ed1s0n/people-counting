# People Detector (FastAPI + Next.js + PostgreSQL)

Detects people in uploaded images, draws boxes, stores results, and provides a paginated/searchable history UI.

## Stack
- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: Next.js (App Router)
- Database: PostgreSQL
- Detection: Yolov8 Ultralytics
- Deployment: Docker Compose

## Run

```bash
docker compose up --build

## How to use

1) Clone your repo and drop these files in place (exact structure above).  
2) Run `docker compose up --build`.  
3) Visit `http://localhost:3000` to upload an image; results appear with bounding boxes + count.  
4) Visit `http://localhost:3000/history` to browse/search/filter past records (pagination included).  