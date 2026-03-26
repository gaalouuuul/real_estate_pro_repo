def register(client, first_name, last_name, email, password, role="user"):
    return client.post("/auth/register", json={
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "role": role,
    })


def login(client, email, password):
    return client.post("/auth/login", json={"email": email, "password": password})


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_auth_and_property_flow(client):
    register(client, "Ahmed", "Owner", "owner@test.com", "secret12", role="owner")
    register(client, "Sara", "Viewer", "viewer@test.com", "secret12", role="user")

    owner_token = login(client, "owner@test.com", "secret12").get_json()["access_token"]
    viewer_token = login(client, "viewer@test.com", "secret12").get_json()["access_token"]

    create_resp = client.post("/properties", headers=auth_header(owner_token), json={
        "name": "Loft Paris",
        "description": "Très lumineux",
        "city": "Paris",
        "type": "loft",
        "price": 500000,
        "surface": 85,
    })
    assert create_resp.status_code == 201
    property_id = create_resp.get_json()["id"]

    room_resp = client.post(f"/properties/{property_id}/rooms", headers=auth_header(owner_token), json={"name": "Salon", "size": 25})
    assert room_resp.status_code == 201

    publish_resp = client.patch(f"/properties/{property_id}/publish", headers=auth_header(owner_token))
    assert publish_resp.status_code == 200
    assert publish_resp.get_json()["status"] == "published"

    favorite_resp = client.post(f"/properties/{property_id}/favorite", headers=auth_header(viewer_token))
    assert favorite_resp.status_code == 201

    visit_resp = client.post(f"/properties/{property_id}/visit-requests", headers=auth_header(viewer_token), json={"requested_at": "2026-04-10T14:00:00", "message": "Available in the afternoon"})
    assert visit_resp.status_code == 201
    visit_id = visit_resp.get_json()["id"]

    accept_resp = client.patch(f"/properties/visit-requests/{visit_id}/status", headers=auth_header(owner_token), json={"status": "accepted"})
    assert accept_resp.status_code == 200
    assert accept_resp.get_json()["status"] == "accepted"

    list_resp = client.get("/properties?city=Paris&published_only=true&sort_by=price&sort_order=desc")
    assert list_resp.status_code == 200
    assert list_resp.get_json()["total"] == 1


def test_admin_stats(client):
    register(client, "Admin", "Root", "admin@test.com", "secret12", role="admin")
    token = login(client, "admin@test.com", "secret12").get_json()["access_token"]
    response = client.get("/admin/stats", headers=auth_header(token))
    assert response.status_code == 200
    assert "active_properties" in response.get_json()
