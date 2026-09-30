def test_get_students(client, auth_headers):
    response = client.get("/students/", headers=auth_headers)
    assert response.status_code == 200