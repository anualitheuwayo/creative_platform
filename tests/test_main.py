from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
)


def test_home_endpoint():
    response = client.get(
        "/",
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to the Creative Marketplace API",
    }


def test_openapi_schema_is_available():
    response = client.get(
        "/openapi.json",
    )

    assert response.status_code == 200

    openapi_schema = response.json()

    assert openapi_schema["info"]["title"] == (
        "Creative Marketplace API"
    )


def test_swagger_docs_are_available():
    response = client.get(
        "/docs",
    )

    assert response.status_code == 200


def test_artwork_router_is_registered():
    response = client.get(
        "/openapi.json",
    )

    openapi_schema = response.json()
    paths = openapi_schema["paths"]

    assert "/api/v1/artworks" in paths

    assert "/api/v1/artworks/{artwork_id}" in paths


def test_artwork_image_upload_route_is_registered():
    response = client.get(
        "/openapi.json",
    )

    openapi_schema = response.json()
    paths = openapi_schema["paths"]

    assert (
        "/api/v1/artworks/{artwork_id}/image"
        in paths
    )


def test_artist_profile_router_is_registered():
    response = client.get(
        "/openapi.json",
    )

    openapi_schema = response.json()
    paths = openapi_schema["paths"]

    assert "/api/v1/artist-profiles" in paths

    assert "/api/v1/artist-profiles/me" in paths


def test_artist_profile_image_upload_route_is_registered():
    response = client.get(
        "/openapi.json",
    )

    openapi_schema = response.json()
    paths = openapi_schema["paths"]

    assert (
        "/api/v1/artist-profiles/me/image"
        in paths
    )


def test_booking_router_is_registered():
    response = client.get(
        "/openapi.json",
    )

    assert response.status_code == 200

    openapi_schema = response.json()
    paths = openapi_schema["paths"]

    assert any(
        path.startswith("/api/v1/bookings")
        for path in paths
    )


def test_notification_router_is_registered():
    response = client.get(
        "/openapi.json",
    )

    openapi_schema = response.json()
    paths = openapi_schema["paths"]

    assert "/api/v1/notifications/me" in paths