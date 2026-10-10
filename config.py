import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR / "workspace"

UPLOAD_DIR = WORKSPACE_DIR / "uploads"
AUDIO_DIR = WORKSPACE_DIR / "audio"
OUTPUT_DIR = WORKSPACE_DIR / "outputs"
TEMP_DIR = WORKSPACE_DIR / "temp"

MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".webm",
    ".avi",
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "development-only-change-this-key",
)


def create_workspace():
    """Create required working directories."""
    for directory in (
        WORKSPACE_DIR,
        UPLOAD_DIR,
        AUDIO_DIR,
        OUTPUT_DIR,
        TEMP_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
