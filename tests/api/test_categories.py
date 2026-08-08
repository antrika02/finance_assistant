from tests.factories import category_payload


def test_create_category(
    client,
    authenticated_headers,
):
    response = client.post(
        "/categories/",
        json=category_payload(),
        headers=authenticated_headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Food"
    assert body["type"] == "expense"
    assert body["icon"] == "🍕"
    assert body["color"] == "#FF5733"


def test_get_categories(
    client,
    authenticated_headers,
):
    client.post(
        "/categories/",
        json=category_payload(),
        headers=authenticated_headers,
    )

    response = client.get(
        "/categories/",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["name"] == "Food"


def test_get_category_by_id(
    client,
    authenticated_headers,
):
    create_response = client.post(
        "/categories/",
        json=category_payload(),
        headers=authenticated_headers,
    )

    category_id = create_response.json()["id"]

    response = client.get(
        f"/categories/{category_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json()["id"] == category_id


def test_update_category(
    client,
    authenticated_headers,
):
    create_response = client.post(
        "/categories/",
        json=category_payload(),
        headers=authenticated_headers,
    )

    category_id = create_response.json()["id"]

    response = client.put(
        f"/categories/{category_id}",
        json={"name": "Groceries"},
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json()["name"] == "Groceries"


def test_delete_category(
    client,
    authenticated_headers,
):
    create_response = client.post(
        "/categories/",
        json=category_payload(),
        headers=authenticated_headers,
    )

    category_id = create_response.json()["id"]

    response = client.delete(
        f"/categories/{category_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/categories/{category_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_get_invalid_category(
    client,
    authenticated_headers,
):
    response = client.get(
        "/categories/99999",
        headers=authenticated_headers,
    )

    assert response.status_code == 404
