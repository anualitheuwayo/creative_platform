import io
from pathlib import Path

def test_get_artworks_returns_list(client):
    response = client.get(
        "/api/v1/artworks",
    )

    assert response.status_code == 200
    assert isinstance(
        response.json(),
        list,
    )


def test_get_artwork_returns_one_artwork(
    client,
    artwork,
):
    response = client.get(
        f"/api/v1/artworks/{artwork.artwork_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["artwork_id"] == artwork.artwork_id
    assert body["title"] == "Test Artwork"
    assert body["artist_id"] == artwork.artist_id
    assert body["image_url"] == (
        "https://example.com/test-artwork.jpg"
    )


def test_get_missing_artwork_returns_404(client):
    response = client.get(
        "/api/v1/artworks/999999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Artwork not found."


def test_artist_can_create_artwork(
    client,
    artist_token_headers,
):
    response = client.post(
        "/api/v1/artworks",
        headers=artist_token_headers,
        json={
            "title": "Sunset in Nairobi",
            "description": "A digital landscape artwork.",
            "price": 2500.00,
            "image_url": None,
            "category": "Digital Art",
            "is_available": True,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Sunset in Nairobi"
    assert body["description"] == (
        "A digital landscape artwork."
    )
    assert body["price"] == "2500.00"
    assert body["image_url"] is None
    assert body["category"] == "Digital Art"
    assert body["is_available"] is True

def test_client_cannot_create_artwork(
    client,
    client_token_headers,
):
    response = client.post(
        "/api/v1/artworks",
        headers=client_token_headers,
        json={
            "title": "Unauthorized Artwork",
            "description": "A Client must not create Artworks.",
            "price": 1000.00,
            "image_url": None,
            "category": "Digital Art",
            "is_available": True,
        },
    )

    assert response.status_code == 403


def test_artwork_owner_can_update_artwork(
    client,
    artwork,
    artist_token_headers,
):
    response = client.patch(
        f"/api/v1/artworks/{artwork.artwork_id}",
        headers=artist_token_headers,
        json={
            "title": "Updated Test Artwork",
            "price": 150.00,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["title"] == "Updated Test Artwork"
    assert body["price"] == "150.00"

    assert body["description"] == (
        "Artwork created for favourite endpoint tests."
    )
    assert body["category"] == "Digital Art"
    assert body["is_available"] is True


def test_client_cannot_update_artwork(
    client,
    artwork,
    client_token_headers,
):
    response = client.patch(
        f"/api/v1/artworks/{artwork.artwork_id}",
        headers=client_token_headers,
        json={
            "title": "Unauthorized Update",
        },
    )

    assert response.status_code == 403


def test_artwork_owner_can_delete_artwork(
    client,
    artwork,
    artist_token_headers,
):
    artwork_id = artwork.artwork_id

    response = client.delete(
        f"/api/v1/artworks/{artwork_id}",
        headers=artist_token_headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/artworks/{artwork_id}",
    )

    assert get_response.status_code == 404


def test_client_cannot_delete_artwork(
    client,
    artwork,
    client_token_headers,
):
    response = client.delete(
        f"/api/v1/artworks/{artwork.artwork_id}",
        headers=client_token_headers,
    )

    assert response.status_code == 403

def test_artwork_owner_can_upload_jpeg_image(
    client,
    artwork,
    artist_token_headers,
):
    image_content = b"\xff\xd8\xff\xe0" + b"test-jpeg-image-content"

    response = client.post(
        f"/api/v1/artworks/{artwork.artwork_id}/image",
        headers=artist_token_headers,
        files={
            "image": (
                "test-artwork.jpg",
                io.BytesIO(image_content),
                "image/jpeg",
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["artwork_id"] == artwork.artwork_id
    assert body["image_url"].startswith(
        "/uploads/artwork-images/"
    )
    assert body["image_url"].endswith(
        ".jpg"
    )

    image_path = Path(
        body["image_url"].lstrip("/")
    )

    assert image_path.exists()

    image_path.unlink()   
    
def test_client_cannot_upload_artwork_image(
    client,
    artwork,
    client_token_headers,
):
    response = client.post(
        f"/api/v1/artworks/{artwork.artwork_id}/image",
        headers=client_token_headers,
        files={
            "image": (
                "client-image.jpg",
                io.BytesIO(b"fake-image"),
                "image/jpeg",
            ),
        },
    )

    assert response.status_code == 403     
    
def test_artwork_image_upload_rejects_pdf(
    client,
    artwork,
    artist_token_headers,
):
    response = client.post(
        f"/api/v1/artworks/{artwork.artwork_id}/image",
        headers=artist_token_headers,
        files={
            "image": (
                "document.pdf",
                io.BytesIO(b"%PDF-1.4 fake content"),
                "application/pdf",
            ),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Only JPEG, PNG, and WEBP images are allowed."
    )    
    
def test_upload_image_for_missing_artwork_returns_404(
    client,
    artist_token_headers,
):
    response = client.post(
        "/api/v1/artworks/999999/image",
        headers=artist_token_headers,
        files={
            "image": (
                "missing-artwork.jpg",
                io.BytesIO(b"fake-image"),
                "image/jpeg",
            ),
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Artwork not found."    