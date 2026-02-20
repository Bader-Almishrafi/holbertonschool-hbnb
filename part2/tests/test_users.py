def test_create_user_ok(client):
    res = client.post("/api/v1/users/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data
    assert data["email"] == "jane.doe@example.com"


def test_create_user_invalid_email(client):
    res = client.post("/api/v1/users/", json={
        "first_name": "A",
        "last_name": "B",
        "email": "bad-email"
    })
    assert res.status_code == 400


def test_get_user_not_found(client):
    res = client.get("/api/v1/users/not-a-real-id")
    assert res.status_code == 404