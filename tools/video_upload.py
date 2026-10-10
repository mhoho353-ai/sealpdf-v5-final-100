from core.file_manager import save_uploaded_video


def process_upload(file_storage):
    """
    Save an uploaded video and return its basic information.
    """
    saved_path = save_uploaded_video(file_storage)

    return {
        "success": True,
        "message": "تم رفع الفيديو بنجاح.",
        "filename": saved_path.name,
        "path": str(saved_path),
        "size_bytes": saved_path.stat().st_size,
    }
