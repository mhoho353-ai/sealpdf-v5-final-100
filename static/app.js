"use strict";

const uploadForm = document.getElementById("upload-form");
const videoInput = document.getElementById("video-file");
const uploadStatus = document.getElementById("upload-status");
const toolOutput = document.getElementById("tool-output");

let currentFilename = null;

async function readResponse(response) {
    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error("استجاب الخادم ببيانات غير صالحة.");
    }

    if (!response.ok || data.success === false) {
        throw new Error(
            data.error || `فشل الطلب: ${response.status}`
        );
    }

    return data;
}

function showOutput(data) {
    toolOutput.textContent = JSON.stringify(data, null, 2);
}

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = videoInput.files[0];

    if (!file) {
        uploadStatus.textContent = "اختر ملف فيديو أولًا.";
        return;
    }

    const formData = new FormData();
    formData.append("video", file);

    uploadStatus.textContent = "جارٍ رفع الفيديو...";

    try {
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData,
        });

        const data = await readResponse(response);

        currentFilename = data.filename;

        uploadStatus.textContent =
            `تم رفع الملف: ${data.filename}`;

        showOutput(data);
    } catch (error) {
        uploadStatus.textContent = error.message;
    }
});

document.querySelectorAll("[data-tool]").forEach((button) => {
    button.addEventListener("click", async () => {
        const tool = button.dataset.tool;

        if (tool === "video_upload") {
            videoInput.focus();
            return;
        }

        if (tool === "video_info") {
            if (!currentFilename) {
                toolOutput.textContent =
                    "ارفع فيديو أولًا قبل قراءة معلوماته.";
                return;
            }

            const formData = new FormData();
            formData.append("filename", currentFilename);

            toolOutput.textContent =
                "جارٍ قراءة معلومات الفيديو...";

            try {
                const response = await fetch("/api/video-info", {
                    method: "POST",
                    body: formData,
                });

                const data = await readResponse(response);

                showOutput(data.info);
            } catch (error) {
                toolOutput.textContent = error.message;
            }

            return;
        }

        toolOutput.textContent =
            "هذه الأداة لم تُنفذ بعد.";
    });
});
