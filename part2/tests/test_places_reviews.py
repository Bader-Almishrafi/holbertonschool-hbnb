def create_user(client, email="owner@example.com"):
    r = client.post("/api/v1/users/", json={
        "first_name": "Owner",
        "last_name": "One",
        "email": email
    })
    assert r.status_code == 201
    return r.get_json()["id"]


def create_amenity(client, name="Wi-Fi"):
    r = client.post("/api/v1/amenities/", json={"name": name})
    assert r.status_code == 201
    return r.get_json()["id"]


def create_place(client, user_id, amenity_id):
    r = client.post("/api/v1/places/", json={
        "title": "Cozy",
        "description": "Nice",
        "price": 100,
        "latitude": 10.0,
        "longitude": 10.0,
        "owner_id": user_id,
        "amenities": [amenity_id]
    })
    assert r.status_code == 201
    return r.get_json()["id"]


def test_create_place_invalid_lat(client):
    user_id = create_user(client, email="lat@test.com")
    amenity_id = create_amenity(client, name="Parking")

    r = client.post("/api/v1/places/", json={
        "title": "Bad",
        "description": "x",
        "price": 100,
        "latitude": 200.0,
        "longitude": 10.0,
        "owner_id": user_id,
        "amenities": [amenity_id]
    })
    assert r.status_code == 400


def test_review_crud_flow(client):
    user_id = create_user(client, email="rev@test.com")
    amenity_id = create_amenity(client, name="AC")
    place_id = create_place(client, user_id, amenity_id)

    # create review
    r = client.post("/api/v1/reviews/", json={
        "text": "Great",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert r.status_code == 201
    review_id = r.get_json()["id"]

    # list reviews by place
    r = client.get(f"/api/v1/places/{place_id}/reviews")
    assert r.status_code == 200
    assert any(x["id"] == review_id for x in r.get_json())

    # update review (your API expects full model, but facade updates only text/rating)
    r = client.put(f"/api/v1/reviews/{review_id}", json={
        "text": "Updated",
        "rating": 4,
        "user_id": user_id,
        "place_id": place_id
    })
    assert r.status_code == 200

    # delete review
    r = client.delete(f"/api/v1/reviews/{review_id}")
    assert r.status_code == 200

    # ensure deleted
    r = client.get(f"/api/v1/reviews/{review_id}")
    assert r.status_code == 404