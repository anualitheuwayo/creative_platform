from uuid import uuid4


def make_test_email(
    prefix: str,
) -> str:
    return f"{prefix}-{uuid4().hex}@example.com"


def register_user(
    client,
    full_name: str,
    email: str,
    password: str,
    role: str,
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
    email: str,
    password: str,
) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    body = response.json()
    token = body["access_token"]

    assert token
    assert body["token_type"] == "bearer"

    return {
        "Authorization": f"Bearer {token}",
    }


def test_login_returns_access_token(client):
    email = make_test_email(
        "artist-login",
    )

    register_user(
        client=client,
        full_name="Amina Hassan",
        email=email,
        password="creative123",
        role="artist",
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "creative123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_rejects_wrong_password(client):
    email = make_test_email(
        "artist-wrong-password",
    )

    register_user(
        client=client,
        full_name="Amina Hassan",
        email=email,
        password="creative123",
        role="artist",
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Incorrect email or password."
    )


def test_login_rejects_unknown_email(client):
    email = make_test_email(
        "unknown-user",
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "creative123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Incorrect email or password."
    )


def test_get_my_profile(client):
    email = make_test_email(
        "artist-profile",
    )

    registered_user = register_user(
        client=client,
        full_name="Amina Hassan",
        email=email,
        password="creative123",
        role="artist",
    )

    headers = login_user(
        client=client,
        email=email,
        password="creative123",
    )

    response = client.get(
        "/api/v1/users/me",
        headers=headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == registered_user["user_id"]
    assert body["email"] == email
    assert body["role"] == "artist"
    assert "password_hash" not in body
    assert "password" not in body


def test_get_my_profile_requires_token(client):
    response = client.get(
        "/api/v1/users/me",
    )

    assert response.status_code == 401