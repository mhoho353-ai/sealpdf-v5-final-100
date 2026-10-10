import json
import shutil
import subprocess
from pathlib import Path


def get_video_info(video_path):
    """
    Return video metadata using ffprobe.

    Raises:
        FileNotFoundError: If the video or ffprobe is missing.
        RuntimeError: If ffprobe cannot inspect the video.
    """
    path = Path(video_path).resolve()

    if not path.is_file():
        raise FileNotFoundError("ملف الفيديو غير موجود.")

    ffprobe = shutil.which("ffprobe")

    if not ffprobe:
        raise RuntimeError(
            "ffprobe غير مثبت أو غير موجود في PATH."
        )

    command = [
        ffprobe,
        "-v", "error",
        "-show_entries",
        "format=duration,size,format_name:"
        "stream=codec_type,codec_name,width,height,"
        "avg_frame_rate,sample_rate,channels",
        "-of", "json",
        str(path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "تعذر تحليل الفيديو."
        )

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "تعذر قراءة نتائج تحليل الفيديو."
        ) from exc

    video_stream = next(
        (
            stream
            for stream in data.get("streams", [])
            if stream.get("codec_type") == "video"
        ),
        None,
    )

    if video_stream is None:
        raise RuntimeError("الملف لا يحتوي على مسار فيديو.")

    format_info = data.get("format", {})

    try:
        duration = float(format_info.get("duration", 0))
    except (TypeError, ValueError):
        duration = 0.0

    try:
        size_bytes = int(
            format_info.get("size", path.stat().st_size)
        )
    except (TypeError, ValueError):
        size_bytes = path.stat().st_size

    return {
        "filename": path.name,
        "duration_seconds": duration,
        "size_bytes": size_bytes,
        "format": format_info.get("format_name"),
        "video_codec": video_stream.get("codec_name"),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "frame_rate": video_stream.get("avg_frame_rate"),
    }
