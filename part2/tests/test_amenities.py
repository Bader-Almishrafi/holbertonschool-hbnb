def test_create_amenity_ok(client):
    res = client.post("/api/v1/amenities/", json={"name": "Wi-Fi"})
    assert res.status_code == 201
    assert "id" in res.get_json()


def test_create_amenity_empty_name(client):
    res = client.post("/api/v1/amenities/", json={"name": ""})
    assert res.status_code == 400