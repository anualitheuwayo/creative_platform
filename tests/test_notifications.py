from fastapi import status


def test_user_can_get_own_notifications(
    client,
    client_token_headers,
    notification,
):
    response = client.get(
        "/api/v1/notifications/me",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["notification_id"] == (
        notification.notification_id
    )
    assert data[0]["message"] == "Test notification message."
    assert data[0]["is_read"] is False


def test_user_can_mark_own_notification_as_read(
    client,
    client_token_headers,
    notification,
):
    response = client.patch(
        f"/api/v1/notifications/"
        f"{notification.notification_id}/read",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["notification_id"] == notification.notification_id
    assert data["is_read"] is True


def test_user_cannot_mark_another_users_notification_as_read(
    client,
    artist_token_headers,
    notification,
):
    response = client.patch(
        f"/api/v1/notifications/"
        f"{notification.notification_id}/read",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You can only update your own notifications."
    }


def test_cannot_mark_nonexistent_notification_as_read(
    client,
    client_token_headers,
):
    response = client.patch(
        "/api/v1/notifications/99999/read",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Notification not found."
    }


def test_notifications_require_authentication(
    client,
):
    response = client.get(
        "/api/v1/notifications/me",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
def test_user_only_sees_own_notifications(
    client,
    artist_token_headers,
    notification,
):
    response = client.get(
        "/api/v1/notifications/me",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []    
    
def test_mark_notification_as_read_requires_authentication(
    client,
    notification,
):
    response = client.patch(
        f"/api/v1/notifications/"
        f"{notification.notification_id}/read",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED    