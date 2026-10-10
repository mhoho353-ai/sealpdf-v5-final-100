TOOLS = {
    "video_upload": {
        "name": "رفع الفيديو",
        "description": "حفظ ملف الفيديو داخل مساحة العمل.",
        "endpoint": "/api/upload",
        "enabled": True,
    },
    "video_info": {
        "name": "معلومات الفيديو",
        "description": "قراءة مدة الفيديو ودقته وخصائصه.",
        "endpoint": "/api/video-info",
        "enabled": True,
    },
    "audio_extract": {
        "name": "استخراج الصوت",
        "description": "استخراج الصوت من الفيديو.",
        "endpoint": "/api/extract-audio",
        "enabled": False,
    },
    "silence_detect": {
        "name": "اكتشاف الصمت",
        "description": "تحديد فترات الصمت داخل الصوت.",
        "endpoint": "/api/detect-silence",
        "enabled": False,
    },
    "silence_remove": {
        "name": "حذف الصمت",
        "description": "حذف فترات الصمت المحددة.",
        "endpoint": "/api/remove-silence",
        "enabled": False,
    },
    "speech_to_text": {
        "name": "تحويل الكلام إلى نص",
        "description": "استخراج الكلام من الفيديو إلى نص.",
        "endpoint": "/api/transcribe",
        "enabled": False,
    },
}


def get_tools():
    """Return a copy of the registered tools."""
    return {
        tool_id: tool.copy()
        for tool_id, tool in TOOLS.items()
    }
