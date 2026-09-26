from io import BytesIO
from pathlib import Path


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


def login_user(
    client,
    email,
    password,
):
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


def artist_profile_payload(
    phone_number="+254712345678",
    show_phone_number=False,
):
    return {
        "bio": (
            "I am a digital artist who creates illustrations, "
            "branding materials, and visual designs."
        ),
        "specialization": "Digital Illustration",
        "location": "Nairobi",
        "hourly_rate": 2500.00,
        "profile_image_url": (
            "https://example.com/images/artist-profile.jpg"
        ),
        "phone_number": phone_number,
        "show_phone_number": show_phone_number,
    }


def create_artist_and_login(
    client,
    full_name="Amina Hassan",
    email="amina@example.com",
    password="creative123",
):
    artist = register_user(
        client=client,
        full_name=full_name,
        email=email,
        password=password,
        role="artist",
    )

    headers = login_user(
        client=client,
        email=email,
        password=password,
    )

    return artist, headers


def create_artist_profile(
    client,
    headers,
    phone_number="+254712345678",
    show_phone_number=False,
):
    response = client.post(
        "/api/v1/artist-profiles",
        json=artist_profile_payload(
            phone_number=phone_number,
            show_phone_number=show_phone_number,
        ),
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()


def test_create_artist_profile(client):
    artist, headers = create_artist_and_login(client)

    response = client.post(
        "/api/v1/artist-profiles",
        json=artist_profile_payload(),
        headers=headers,
    )

    assert response.status_code == 201

    profile = response.json()

    assert profile["artist_profile_id"] is not None
    assert profile["artist_id"] == artist["user_id"]
    assert profile["bio"].startswith("I am a digital artist")
    assert profile["specialization"] == "Digital Illustration"
    assert profile["location"] == "Nairobi"
    assert float(profile["hourly_rate"]) == 2500.00
    assert profile["profile_image_url"] == (
        "https://example.com/images/artist-profile.jpg"
    )
    assert profile["phone_number"] == "+254712345678"
    assert profile["show_phone_number"] is False
    assert profile["is_verified"] is False


def test_create_artist_profile_requires_token(client):
    response = client.post(
        "/api/v1/artist-profiles",
        json=artist_profile_payload(),
    )

    assert response.status_code == 401


def test_client_cannot_create_artist_profile(client):
    register_user(
        client=client,
        full_name="James Mwangi",
        email="james@example.com",
        password="clientpass123",
        role="client",
    )

    headers = login_user(
        client=client,
        email="james@example.com",
        password="clientpass123",
    )

    response = client.post(
        "/api/v1/artist-profiles",
        json=artist_profile_payload(),
        headers=headers,
    )

    assert response.status_code == 403


def test_artist_cannot_create_two_profiles(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.post(
        "/api/v1/artist-profiles",
        json=artist_profile_payload(),
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Artist profile already exists."
    )


def test_get_artist_profiles(client):
    artist, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.get(
        "/api/v1/artist-profiles",
    )

    assert response.status_code == 200

    profiles = response.json()

    assert len(profiles) == 1
    assert profiles[0]["artist_profile_id"] == (
        profile["artist_profile_id"]
    )
    assert profiles[0]["artist_id"] == artist["user_id"]


def test_get_one_artist_profile(client):
    _, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.get(
        "/api/v1/artist-profiles/"
        f"{profile['artist_profile_id']}",
    )

    assert response.status_code == 200

    public_profile = response.json()

    assert public_profile["artist_profile_id"] == (
        profile["artist_profile_id"]
    )
    assert public_profile["specialization"] == (
        "Digital Illustration"
    )


def test_get_missing_artist_profile(client):
    response = client.get(
        "/api/v1/artist-profiles/99999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Artist profile not found."
    )


def test_get_my_artist_profile(client):
    artist, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.get(
        "/api/v1/artist-profiles/me",
        headers=headers,
    )

    assert response.status_code == 200

    my_profile = response.json()

    assert my_profile["artist_profile_id"] == (
        profile["artist_profile_id"]
    )
    assert my_profile["artist_id"] == artist["user_id"]
    assert my_profile["phone_number"] == "+254712345678"
    assert my_profile["show_phone_number"] is False


def test_update_my_artist_profile(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.patch(
        "/api/v1/artist-profiles/me",
        json={
            "location": "Mombasa",
            "hourly_rate": 3000.00,
        },
        headers=headers,
    )

    assert response.status_code == 200

    profile = response.json()

    assert profile["location"] == "Mombasa"
    assert float(profile["hourly_rate"]) == 3000.00
    assert profile["specialization"] == (
        "Digital Illustration"
    )


def test_artist_can_update_phone_number(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.patch(
        "/api/v1/artist-profiles/me",
        json={
            "phone_number": "+254799123456",
        },
        headers=headers,
    )

    assert response.status_code == 200

    profile = response.json()

    assert profile["phone_number"] == "+254799123456"
    assert profile["show_phone_number"] is False


def test_artist_can_enable_phone_number_visibility(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
        show_phone_number=False,
    )

    response = client.patch(
        "/api/v1/artist-profiles/me",
        json={
            "show_phone_number": True,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["show_phone_number"] is True


def test_artist_can_disable_phone_number_visibility(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
        show_phone_number=True,
    )

    response = client.patch(
        "/api/v1/artist-profiles/me",
        json={
            "show_phone_number": False,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["show_phone_number"] is False


def test_public_profile_hides_phone_when_visibility_is_false(
    client,
):
    _, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
        phone_number="+254712345678",
        show_phone_number=False,
    )

    response = client.get(
        "/api/v1/artist-profiles/"
        f"{profile['artist_profile_id']}",
    )

    assert response.status_code == 200

    public_profile = response.json()

    assert public_profile["show_phone_number"] is False
    assert public_profile["phone_number"] is None


def test_public_profile_shows_phone_when_visibility_is_true(
    client,
):
    _, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
        phone_number="+254712345678",
        show_phone_number=True,
    )

    response = client.get(
        "/api/v1/artist-profiles/"
        f"{profile['artist_profile_id']}",
    )

    assert response.status_code == 200

    public_profile = response.json()

    assert public_profile["show_phone_number"] is True
    assert public_profile["phone_number"] == "+254712345678"


def test_public_artist_profiles_hide_private_phone_numbers(
    client,
):
    _, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
        phone_number="+254712345678",
        show_phone_number=False,
    )

    response = client.get(
        "/api/v1/artist-profiles",
    )

    assert response.status_code == 200

    profiles = response.json()

    assert len(profiles) == 1
    assert profiles[0]["artist_profile_id"] == (
        profile["artist_profile_id"]
    )
    assert profiles[0]["phone_number"] is None
    assert profiles[0]["show_phone_number"] is False


def test_public_artist_profiles_show_public_phone_numbers(
    client,
):
    _, headers = create_artist_and_login(client)

    profile = create_artist_profile(
        client=client,
        headers=headers,
        phone_number="+254712345678",
        show_phone_number=True,
    )

    response = client.get(
        "/api/v1/artist-profiles",
    )

    assert response.status_code == 200

    profiles = response.json()

    assert len(profiles) == 1
    assert profiles[0]["artist_profile_id"] == (
        profile["artist_profile_id"]
    )
    assert profiles[0]["phone_number"] == "+254712345678"
    assert profiles[0]["show_phone_number"] is True


def test_delete_my_artist_profile(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    delete_response = client.delete(
        "/api/v1/artist-profiles/me",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        "/api/v1/artist-profiles/me",
        headers=headers,
    )

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == (
        "Artist profile not found."
    )


def test_artist_can_upload_profile_image(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.post(
        "/api/v1/artist-profiles/me/image",
        files={
            "image": (
                "profile.png",
                BytesIO(b"fake-image-content"),
                "image/png",
            ),
        },
        headers=headers,
    )

    assert response.status_code == 200

    profile = response.json()

    assert profile["profile_image_url"] is not None
    assert profile["profile_image_url"].startswith(
        "/uploads/profile-images/"
    )
    assert profile["profile_image_url"].endswith(
        ".png"
    )

    saved_filename = profile["profile_image_url"].split(
        "/"
    )[-1]

    saved_file = Path(
        "uploads/profile-images"
    ) / saved_filename

    assert saved_file.exists()

    saved_file.unlink()


def test_profile_image_upload_requires_profile(client):
    _, headers = create_artist_and_login(client)

    response = client.post(
        "/api/v1/artist-profiles/me/image",
        files={
            "image": (
                "profile.jpg",
                BytesIO(b"fake-image-content"),
                "image/jpeg",
            ),
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Artist profile not found."
    )


def test_profile_image_upload_rejects_invalid_type(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.post(
        "/api/v1/artist-profiles/me/image",
        files={
            "image": (
                "document.pdf",
                BytesIO(b"not-an-image"),
                "application/pdf",
            ),
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Only JPEG, PNG, and WEBP images are allowed."
    )


def test_profile_image_upload_rejects_invalid_extension(client):
    _, headers = create_artist_and_login(client)

    create_artist_profile(
        client=client,
        headers=headers,
    )

    response = client.post(
        "/api/v1/artist-profiles/me/image",
        files={
            "image": (
                "image.pdf",
                BytesIO(b"fake-image-content"),
                "image/png",
            ),
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Invalid image file extension."
    )