from fastapi import status


def test_client_can_create_favourite(
    client,
    client_token_headers,
    client_user,
    artwork,
):
    response = client.post(
        f"/api/v1/favourites/artworks/{artwork.artwork_id}",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["client_id"] == client_user.user_id
    assert data["artwork_id"] == artwork.artwork_id
    assert "favourite_id" in data


def test_client_can_get_own_favourites(
    client,
    client_token_headers,
    favourite,
):
    response = client.get(
        "/api/v1/favourites/me",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["favourite_id"] == favourite.favourite_id
    assert data[0]["client_id"] == favourite.client_id
    assert data[0]["artwork_id"] == favourite.artwork_id


def test_client_cannot_favourite_same_artwork_twice(
    client,
    client_token_headers,
    artwork,
):
    first_response = client.post(
        f"/api/v1/favourites/artworks/{artwork.artwork_id}",
        headers=client_token_headers,
    )

    assert first_response.status_code == status.HTTP_201_CREATED

    second_response = client.post(
        f"/api/v1/favourites/artworks/{artwork.artwork_id}",
        headers=client_token_headers,
    )

    assert second_response.status_code == status.HTTP_400_BAD_REQUEST
    assert second_response.json() == {
        "detail": "Artwork is already in your favourites."
    }


def test_client_can_delete_own_favourite(
    client,
    client_token_headers,
    favourite,
):
    response = client.delete(
        f"/api/v1/favourites/{favourite.favourite_id}",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_deleted_favourite_is_not_in_my_favourites(
    client,
    client_token_headers,
    favourite,
):
    delete_response = client.delete(
        f"/api/v1/favourites/{favourite.favourite_id}",
        headers=client_token_headers,
    )

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(
        "/api/v1/favourites/me",
        headers=client_token_headers,
    )

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == []


def test_artist_cannot_use_favourite_endpoints(
    client,
    artist_token_headers,
    artwork,
):
    response = client.post(
        f"/api/v1/favourites/artworks/{artwork.artwork_id}",
        headers=artist_token_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Only clients can perform this action."
    }


def test_cannot_favourite_nonexistent_artwork(
    client,
    client_token_headers,
):
    response = client.post(
        "/api/v1/favourites/artworks/99999",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Artwork not found."
    }


def test_client_cannot_delete_nonexistent_favourite(
    client,
    client_token_headers,
):
    response = client.delete(
        "/api/v1/favourites/99999",
        headers=client_token_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Favourite not found."
    }