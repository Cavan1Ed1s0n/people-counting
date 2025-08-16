from pathlib import Path
from ..core.config import settings

def ensure_storage() -> Path:
    p = Path(settings.STORAGE_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p
