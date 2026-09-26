from datetime import date, timedelta

from fastapi import status


def test_artist_can_create_availability(
    client,
    artist_token_headers,
    artist_user,
):
    response = client.post(
        "/api/v1/availabilities/",
        headers=artist_token_headers,
        json={
            "available_date": str(
                date.today() + timedelta(days=7)
            ),
            "start_time": "09:00:00",
            "end_time": "12:00:00",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["artist_id"] == artist_user.user_id
    assert data["is_available"] is True
    assert data["start_time"] == "09:00:00"
    assert data["end_time"] == "12:00:00"


def test_artist_can_get_own_availabilities(
    client,
    artist_token_headers,
    availability,
):
    response = client.get(
        "/api/v1/availabilities/me",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["availability_id"] == (
        availability.availability_id
    )


def test_public_can_get_artist_available_slots(
    client,
    availability,
):
    response = client.get(
        f"/api/v1/availabilities/artist/{availability.artist_id}"
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["availability_id"] == (
        availability.availability_id
    )
    assert data[0]["is_available"] is True


def test_client_cannot_create_availability(
    client,
    client_token_headers,
):
    response = client.post(
        "/api/v1/availabilities/",
        headers=client_token_headers,
        json={
            "available_date": str(
                date.today() + timedelta(days=7)
            ),
            "start_time": "09:00:00",
            "end_time": "12:00:00",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Only artists can perform this action."
    }


def test_cannot_create_availability_in_the_past(
    client,
    artist_token_headers,
):
    response = client.post(
        "/api/v1/availabilities/",
        headers=artist_token_headers,
        json={
            "available_date": str(
                date.today() - timedelta(days=1)
            ),
            "start_time": "09:00:00",
            "end_time": "12:00:00",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Availability date cannot be in the past."
    }


def test_cannot_create_availability_with_invalid_time_range(
    client,
    artist_token_headers,
):
    response = client.post(
        "/api/v1/availabilities/",
        headers=artist_token_headers,
        json={
            "available_date": str(
                date.today() + timedelta(days=7)
            ),
            "start_time": "14:00:00",
            "end_time": "09:00:00",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_artist_can_update_own_availability(
    client,
    artist_token_headers,
    availability,
):
    response = client.patch(
        f"/api/v1/availabilities/{availability.availability_id}",
        headers=artist_token_headers,
        json={
            "start_time": "10:00:00",
            "end_time": "13:00:00",
            "is_available": False,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["start_time"] == "10:00:00"
    assert data["end_time"] == "13:00:00"
    assert data["is_available"] is False


def test_artist_can_delete_own_availability(
    client,
    artist_token_headers,
    availability,
):
    response = client.delete(
        f"/api/v1/availabilities/{availability.availability_id}",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT