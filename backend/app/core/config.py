import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = BASE_DIR.parent

# Load .env from repo root first, then backend/ (backend wins on duplicate keys).
load_dotenv(REPO_ROOT / ".env", override=False)
load_dotenv(BASE_DIR / ".env", override=True)

DB_PATH = os.getenv("LUCALIVE_DB_PATH", str(BASE_DIR / "lucalive.db"))

POLL_INTERVAL_SECONDS = int(os.getenv("LUCALIVE_POLL_INTERVAL", "60"))

CORS_ORIGINS = os.getenv("LUCALIVE_CORS_ORIGINS", "http://localhost:5173").split(",")

DOUYINLIVERECORDER_PATH = str(BASE_DIR / "DouyinLiveRecorder")

def get_douyu_cookies() -> str | None:
    """Read each time so a restarted worker picks up env/.env changes."""
    v = os.getenv("LUCALIVE_DOUYU_COOKIES", "")
    if not isinstance(v, str):
        return None
    v = v.strip().strip('"').strip("'")
    return v or None
