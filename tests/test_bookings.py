from fastapi import status


def test_client_can_create_booking(
    client,
    client_token_headers,
    client_user,
    availability,
):
    response = client.post(
        "/api/v1/bookings/",
        headers=client_token_headers,
        json={
            "availability_id": availability.availability_id,
            "message": "I would like to book this slot.",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["client_id"] == client_user.user_id
    assert data["artist_id"] == availability.artist_id
    assert data["availability_id"] == (
        availability.availability_id
    )
    assert data["message"] == "I would like to book this slot."
    assert data["status"] == "pending"


def test_booking_makes_availability_unavailable(
    client,
    client_token_headers,
    availability,
):
    response = client.post(
        "/api/v1/bookings/",
        headers=client_token_headers,
        json={
            "availability_id": availability.availability_id,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    slots_response = client.get(
        f"/api/v1/availabilities/artist/{availability.artist_id}"
    )

    assert slots_response.status_code == status.HTTP_200_OK
    assert slots_response.json() == []


def test_client_cannot_book_unavailable_slot(
    client,
    client_token_headers,
    booking,
):
    response = client.post(
        "/api/v1/bookings/",
        headers=client_token_headers,
        json={
            "availability_id": booking.availability_id,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Availability slot is no longer available."
    }


def test_artist_cannot_create_booking(
    client,
    artist_token_headers,
    availability,
):
    response = client.post(
        "/api/v1/bookings/",
        headers=artist_token_headers,
        json={
            "availability_id": availability.availability_id,
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Only clients can perform this action."
    }


def test_client_can_get_own_bookings(
    client,
    client_token_headers,
    booking,
):
    response = client.get(
        "/api/v1/bookings/me/client",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["booking_id"] == booking.booking_id


def test_artist_can_get_assigned_bookings(
    client,
    artist_token_headers,
    booking,
):
    response = client.get(
        "/api/v1/bookings/me/artist",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["booking_id"] == booking.booking_id
    assert data[0]["artist_id"] == booking.artist_id


def test_artist_can_accept_own_booking(
    client,
    artist_token_headers,
    booking,
):
    response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=artist_token_headers,
        json={
            "status": "accepted",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "accepted"


def test_client_can_cancel_own_booking(
    client,
    client_token_headers,
    booking,
):
    response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/cancel",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "cancelled"


def test_rejected_booking_reopens_availability(
    client,
    artist_token_headers,
    booking,
):
    response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=artist_token_headers,
        json={
            "status": "rejected",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "rejected"

    slots_response = client.get(
        f"/api/v1/availabilities/artist/{booking.artist_id}"
    )

    assert slots_response.status_code == status.HTTP_200_OK

    slots = slots_response.json()

    assert len(slots) == 1
    assert slots[0]["availability_id"] == (
        booking.availability_id
    )
    
def test_creating_booking_notifies_artist(
    client,
    client_token_headers,
    artist_token_headers,
    availability,
):
    booking_response = client.post(
        "/api/v1/bookings/",
        headers=client_token_headers,
        json={
            "availability_id": availability.availability_id,
            "message": "I would like to book this slot.",
        },
    )

    assert booking_response.status_code == status.HTTP_201_CREATED

    notifications_response = client.get(
        "/api/v1/notifications/me",
        headers=artist_token_headers,
    )

    assert notifications_response.status_code == status.HTTP_200_OK

    notifications = notifications_response.json()

    assert len(notifications) == 1
    assert notifications[0]["notification_type"] == (
        "booking_created"
    )
    assert notifications[0]["message"] == (
        "You have a new booking request."
    )
    assert notifications[0]["is_read"] is False


def test_accepting_booking_notifies_client(
    client,
    client_token_headers,
    artist_token_headers,
    booking,
):
    accept_response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=artist_token_headers,
        json={
            "status": "accepted",
        },
    )

    assert accept_response.status_code == status.HTTP_200_OK

    notifications_response = client.get(
        "/api/v1/notifications/me",
        headers=client_token_headers,
    )

    assert notifications_response.status_code == status.HTTP_200_OK

    notifications = notifications_response.json()

    assert len(notifications) == 1
    assert notifications[0]["notification_type"] == (
        "booking_accepted"
    )
    assert notifications[0]["message"] == (
        "Your booking has been accepted."
    )


def test_rejecting_booking_notifies_client(
    client,
    client_token_headers,
    artist_token_headers,
    booking,
):
    reject_response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=artist_token_headers,
        json={
            "status": "rejected",
        },
    )

    assert reject_response.status_code == status.HTTP_200_OK

    notifications_response = client.get(
        "/api/v1/notifications/me",
        headers=client_token_headers,
    )

    assert notifications_response.status_code == status.HTTP_200_OK

    notifications = notifications_response.json()

    assert len(notifications) == 1
    assert notifications[0]["notification_type"] == (
        "booking_rejected"
    )
    assert notifications[0]["message"] == (
        "Your booking has been rejected."
    )


def test_cancelling_booking_notifies_artist(
    client,
    client_token_headers,
    artist_token_headers,
    booking,
):
    cancel_response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/cancel",
        headers=client_token_headers,
    )

    assert cancel_response.status_code == status.HTTP_200_OK

    notifications_response = client.get(
        "/api/v1/notifications/me",
        headers=artist_token_headers,
    )

    assert notifications_response.status_code == status.HTTP_200_OK

    notifications = notifications_response.json()

    assert len(notifications) == 1
    assert notifications[0]["notification_type"] == (
        "booking_cancelled"
    )
    assert notifications[0]["message"] == (
        "A client cancelled their booking."
    )    
    
def test_client_cannot_update_booking_status(
    client,
    client_token_headers,
    booking,
):
    response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=client_token_headers,
        json={
            "status": "accepted",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Only artists can perform this action."
    }    
    
def test_artist_cannot_cancel_booking(
    client,
    artist_token_headers,
    booking,
):
    response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/cancel",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Only clients can perform this action."
    }    
    
def test_client_cannot_book_missing_availability(
    client,
    client_token_headers,
):
    response = client.post(
        "/api/v1/bookings/",
        headers=client_token_headers,
        json={
            "availability_id": 999999,
            "message": "This availability does not exist.",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Availability slot not found."
    }

def test_artist_cannot_set_booking_to_cancelled(
    client,
    artist_token_headers,
    booking,
):
    response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=artist_token_headers,
        json={
            "status": "cancelled",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": (
            "Artists can only set booking status to "
            "accepted, rejected, or completed."
        )
    }        
    
def test_artist_cannot_update_cancelled_booking(
    client,
    client_token_headers,
    artist_token_headers,
    booking,
):
    cancel_response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/cancel",
        headers=client_token_headers,
    )

    assert cancel_response.status_code == status.HTTP_200_OK
    assert cancel_response.json()["status"] == "cancelled"

    update_response = client.patch(
        f"/api/v1/bookings/{booking.booking_id}/status",
        headers=artist_token_headers,
        json={
            "status": "accepted",
        },
    )

    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    assert update_response.json() == {
        "detail": "Cancelled bookings cannot be updated."
    }    