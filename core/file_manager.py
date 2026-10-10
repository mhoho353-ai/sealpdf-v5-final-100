from pathlib import Path
from werkzeug.utils import secure_filename

from config import (
    ALLOWED_VIDEO_EXTENSIONS,
    UPLOAD_DIR,
)


def is_allowed_video(filename: str) -> bool:
    """Check the filename extension."""
    if not filename or "." not in filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_VIDEO_EXTENSIONS


def save_uploaded_video(file_storage):
    """
    Save an uploaded file using a sanitized filename.

    Returns:
        Path: Path to the saved file.

    Raises:
        ValueError: If the file is missing or has an invalid extension.
    """
    if file_storage is None:
        raise ValueError("لم يتم إرسال ملف.")

    original_name = file_storage.filename

    if not original_name:
        raise ValueError("اسم الملف فارغ.")

    if not is_allowed_video(original_name):
        raise ValueError("امتداد الفيديو غير مدعوم.")

    safe_name = secure_filename(original_name)

    if not safe_name:
        raise ValueError("تعذر إنشاء اسم آمن للملف.")

    extension = Path(safe_name).suffix.lower()
    destination = UPLOAD_DIR / safe_name

    # Avoid overwriting an existing upload.
    counter = 1

    while destination.exists():
        destination = UPLOAD_DIR / (
            f"{Path(safe_name).stem}_{counter}{extension}"
        )
        counter += 1

    file_storage.save(destination)

    return destination
