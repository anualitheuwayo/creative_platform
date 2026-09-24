def create_user(client, role="artist"):
    response = client.post(
        "/api/v1/users",
        json={
            "full_name": f"Test {role.title()}",
            "email": f"{role}@example.com",
            "password": "creative123",
            "role": role,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_artist_user(client):
    user = create_user(
        client,
        role="artist",
    )

    assert user["user_id"] is not None
    assert user["full_name"] == "Test Artist"
    assert user["email"] == "artist@example.com"
    assert user["role"] == "artist"
    assert user["is_active"] is True
    assert "password" not in user
    assert "password_hash" not in user


def test_create_client_user(client):
    user = create_user(
        client,
        role="client",
    )

    assert user["user_id"] is not None
    assert user["full_name"] == "Test Client"
    assert user["email"] == "client@example.com"
    assert user["role"] == "client"
    assert user["is_active"] is True
    assert "password" not in user
    assert "password_hash" not in user


def test_get_users(client):
    artist = create_user(
        client,
        role="artist",
    )

    client_user = create_user(
        client,
        role="client",
    )

    response = client.get("/api/v1/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 2

    emails = [user["email"] for user in users]

    assert artist["email"] in emails
    assert client_user["email"] in emails


def test_get_one_user(client):
    user = create_user(
        client,
        role="artist",
    )

    response = client.get(
        f"/api/v1/users/{user['user_id']}"
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == user["user_id"]
    assert response.json()["role"] == "artist"


def test_get_missing_user(client):
    response = client.get("/api/v1/users/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


def test_update_user(client):
    user = create_user(
        client,
        role="artist",
    )

    response = client.patch(
        f"/api/v1/users/{user['user_id']}",
        json={
            "full_name": "Updated Artist Studio",
            "is_active": False,
        },
    )

    assert response.status_code == 200

    updated_user = response.json()

    assert updated_user["full_name"] == "Updated Artist Studio"
    assert updated_user["is_active"] is False
    assert updated_user["email"] == "artist@example.com"
    assert updated_user["role"] == "artist"


def test_update_user_role(client):
    user = create_user(
        client,
        role="client",
    )

    response = client.patch(
        f"/api/v1/users/{user['user_id']}",
        json={
            "role": "artist",
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "artist"


def test_duplicate_email(client):
    create_user(
        client,
        role="artist",
    )

    response = client.post(
        "/api/v1/users",
        json={
            "full_name": "Another Artist",
            "email": "artist@example.com",
            "password": "anotherpass123",
            "role": "artist",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A user with this email already exists."
    )


def test_reject_invalid_user_role(client):
    response = client.post(
        "/api/v1/users",
        json={
            "full_name": "Invalid Role User",
            "email": "invalid@example.com",
            "password": "creative123",
            "role": "admin",
        },
    )

    assert response.status_code == 422


def test_delete_user(client):
    user = create_user(
        client,
        role="client",
    )

    delete_response = client.delete(
        f"/api/v1/users/{user['user_id']}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/api/v1/users/{user['user_id']}"
    )

    assert get_response.status_code == 404