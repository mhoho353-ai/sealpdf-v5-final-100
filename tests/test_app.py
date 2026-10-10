import io

import pytest

from app import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"VideoForge AI" in response.data


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


def test_tools_endpoint(client):
    response = client.get("/api/tools")

    assert response.status_code == 200

    data = response.get_json()

    assert "video_upload" in data["tools"]
    assert "video_info" in data["tools"]


def test_upload_rejects_invalid_extension(client):
    response = client.post(
        "/api/upload",
        data={
            "video": (
                io.BytesIO(b"not a video"),
                "document.txt",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False


def test_upload_requires_file(client):
    response = client.post(
        "/api/upload",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
