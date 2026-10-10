from pathlib import Path

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from config import (
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    create_workspace,
)

from core.tool_registry import get_tools
from tools.video_info import get_video_info
from tools.video_upload import process_upload


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = SECRET_KEY

create_workspace()


@app.get("/")
def index():
    return render_template(
        "index.html",
        tools=get_tools(),
    )


@app.get("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "VideoForge AI is running.",
    })


@app.get("/api/tools")
def list_tools():
    return jsonify({
        "success": True,
        "tools": get_tools(),
    })


@app.post("/api/upload")
def upload_video():
    uploaded_file = request.files.get("video")

    try:
        result = process_upload(uploaded_file)

        return jsonify(result), 201

    except ValueError as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 400

    except OSError:
        app.logger.exception("Video upload failed")

        return jsonify({
            "success": False,
            "error": "تعذر حفظ الملف.",
        }), 500


@app.post("/api/video-info")
def video_info():
    filename = request.form.get("filename", "").strip()

    if not filename or Path(filename).name != filename:
        return jsonify({
            "success": False,
            "error": "اسم الملف غير صالح.",
        }), 400

    from config import UPLOAD_DIR

    video_path = UPLOAD_DIR / filename

    try:
        result = get_video_info(video_path)

        return jsonify({
            "success": True,
            "info": result,
        })

    except FileNotFoundError as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 404

    except (RuntimeError, OSError) as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
        }), 422


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({
        "success": False,
        "error": "حجم الملف أكبر من الحد المسموح.",
    }), 413


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )
