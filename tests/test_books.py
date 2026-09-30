def test_get_books(client, auth_headers):
    response = client.get("/books_db", headers=auth_headers)
    # → same pattern jaisa students mein tha: client (fake Postman) + auth_headers (token wala header)

    assert response.status_code == 200
    # → 200 expect, warna FAILED dikhega