def register_user(
    client,
    full_name,
    email,
    password,
    role,
):
    response = client.post(
        "/api/v1/users",
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
            "role": role,
        },
    )

    assert response.status_code == 201

    return response.json()


def login_user(client, email, password):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def artwork_payload():
    return {
        "title": "Sunset Over Nairobi",
        "description": (
            "An original digital illustration inspired "
            "by Nairobi at sunset."
        ),
        "price": 2500.00,
        "image_url": (
            "https://example.com/"
            "sunset-over-nairobi.jpg"
        ),
        "category": "Digital Art",
    }


def create_artist_and_login(client):
    artist = register_user(
        client=client,
        full_name="Amina Hassan",
        email="amina@example.com",
        password="creative123",
        role="artist",
    )

    headers = login_user(
        client,
        email="amina@example.com",
        password="creative123",
    )

    return artist, headers


def test_create_artwork_as_artist(client):
    artist, headers = create_artist_and_login(client)

    response = client.post(
        "/api/v1/artworks",
        json=artwork_payload(),
        headers=headers,
    )

    assert response.status_code == 201

    artwork = response.json()

    assert artwork["artwork_id"] is not None
    assert artwork["title"] == "Sunset Over Nairobi"
    assert artwork["artist_id"] == artist["user_id"]
    assert artwork["is_available"] is True


def test_create_artwork_requires_token(client):
    response = client.post(
        "/api/v1/artworks",
        json=artwork_payload(),
    )

    assert response.status_code == 401


def test_client_cannot_create_artwork(client):
    register_user(
        client=client,
        full_name="James Mwangi",
        email="james@example.com",
        password="clientpass123",
        role="client",
    )

    headers = login_user(
        client,
        email="james@example.com",
        password="clientpass123",
    )

    response = client.post(
        "/api/v1/artworks",
        json=artwork_payload(),
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Only artists can perform this action."
    )


def test_artist_can_update_own_artwork(client):
    _, headers = create_artist_and_login(client)

    create_response = client.post(
        "/api/v1/artworks",
        json=artwork_payload(),
        headers=headers,
    )

    artwork_id = create_response.json()["artwork_id"]

    response = client.patch(
        f"/api/v1/artworks/{artwork_id}",
        json={
            "title": "Updated Sunset Artwork",
            "price": 3000.00,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Sunset Artwork"
    assert float(response.json()["price"]) == 3000.00


def test_artist_cannot_update_another_artists_artwork(client):
    _, first_artist_headers = create_artist_and_login(client)

    create_response = client.post(
        "/api/v1/artworks",
        json=artwork_payload(),
        headers=first_artist_headers,
    )

    artwork_id = create_response.json()["artwork_id"]

    register_user(
        client=client,
        full_name="Brian Otieno",
        email="brian@example.com",
        password="artistpass123",
        role="artist",
    )

    second_artist_headers = login_user(
        client,
        email="brian@example.com",
        password="artistpass123",
    )

    response = client.patch(
        f"/api/v1/artworks/{artwork_id}",
        json={
            "title": "Stolen Artwork Update",
        },
        headers=second_artist_headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only update your own artwork."
    )


def test_artist_can_delete_own_artwork(client):
    _, headers = create_artist_and_login(client)

    create_response = client.post(
        "/api/v1/artworks",
        json=artwork_payload(),
        headers=headers,
    )

    artwork_id = create_response.json()["artwork_id"]

    delete_response = client.delete(
        f"/api/v1/artworks/{artwork_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/artworks/{artwork_id}"
    )

    assert get_response.status_code == 404