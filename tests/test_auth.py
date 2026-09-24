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


def test_login_returns_access_token(client):
    register_user(
        client=client,
        full_name="Amina Hassan",
        email="amina@example.com",
        password="creative123",
        role="artist",
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "amina@example.com",
            "password": "creative123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_rejects_wrong_password(client):
    register_user(
        client=client,
        full_name="Amina Hassan",
        email="amina@example.com",
        password="creative123",
        role="artist",
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "amina@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "missing@example.com",
            "password": "creative123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."


def test_get_my_profile(client):
    registered_user = register_user(
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

    response = client.get(
        "/api/v1/users/me",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == registered_user["user_id"]
    assert response.json()["email"] == "amina@example.com"
    assert response.json()["role"] == "artist"
    assert "password_hash" not in response.json()


def test_get_my_profile_requires_token(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401