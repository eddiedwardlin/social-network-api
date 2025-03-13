import pytest
from jose import jwt
from app import schemas
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [('wrong@gmail.com', 'password123', 403), ('hello123@gmail.com', 'wrong', 403), ('wrong@gmail.com', 'wrong', 403), (None, 'password123', 403), ('wrong@gmail.com', None, 403)])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get('detail') == "Invalid credentials"