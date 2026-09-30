# def test_login_wrong_password(client):
#     client.post("/auth/register", json={"userName": "test1", "password": "correct"})
#     response = client.post("/auth/login", json={"userName": "test1", "password": "wrong"})
#     assert response.status_code == 401


def test_login_wrong_password(client):
    reg = client.post("/auth/register", json={"userName": "test4", "password": "correct"})
    print("REGISTER:", reg.status_code, reg.json())
    # → register sahi gaya ya nahi, pehle yeh confirm karo

    response = client.post("/auth/login", json={"userName": "test4", "password": "wrong"})
    print("LOGIN:", response.status_code, response.json())
    assert response.status_code == 401