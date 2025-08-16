from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.database import Base, engine
from .api.routes_upload import router as upload_router
from .api.routes_history import router as history_router
from .core.config import settings

app = FastAPI(title=settings.APP_NAME)

# CORS: allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init
Base.metadata.create_all(bind=engine)

# Static served files
app.mount("/static", StaticFiles(directory=settings.STORAGE_DIR), name="static")

# Routes
app.include_router(upload_router, prefix=f"{settings.API_PREFIX}")
app.include_router(history_router, prefix=f"{settings.API_PREFIX}")

@app.get("/")
def health():
    return {"status": "ok", "service": settings.APP_NAME}
