def test_students_without_token(client):
    response = client.get("/students/")
    assert response.status_code == 401
    print(response.json())
