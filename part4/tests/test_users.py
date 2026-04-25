def test_create_user_ok(client):
    res = client.post("/api/v1/users/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "password": "secret123"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data
    assert data["email"] == "jane.doe@example.com"
    assert "password" not in data


def test_create_user_invalid_email(client):
    res = client.post("/api/v1/users/", json={
        "first_name": "A",
        "last_name": "B",
        "email": "bad-email",
        "password": "secret123"
    })
    assert res.status_code == 400


def test_get_user_not_found(client):
    res = client.get("/api/v1/users/not-a-real-id")
    assert res.status_code == 404


def test_get_user_never_exposes_password(client):
    create_res = client.post("/api/v1/users/", json={
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "password": "secret123"
    })
    assert create_res.status_code == 201

    user_id = create_res.get_json()["id"]
    get_res = client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == 200
    assert "password" not in get_res.get_json()
