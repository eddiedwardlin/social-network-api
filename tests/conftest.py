from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user_2(client):
    user_data = {"email": "hello1234@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers={**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, test_user_2, session):
    posts_data = [{
        "title": "title 1",
        "content": "content 1",
        "user_id": test_user['id']
    }, {
        "title": "title 2",
        "content": "content 2",
        "user_id": test_user['id']
    }, {
        "title": "title 3",
        "content": "content 3",
        "user_id": test_user['id']
    }, {
        "title": "title 4",
        "content": "content 4",
        "user_id": test_user_2['id']
    }]

    posts_list = list(map(lambda post : models.Post(**post), posts_data))
    session.add_all(posts_list)
    session.commit()
    posts = session.query(models.Post).all()

    return posts
