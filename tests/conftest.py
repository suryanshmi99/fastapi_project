import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db


# Fake/Test Database
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Fake DB dependency
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# FastAPI ko bolo:
# production/original get_db ki jagah fake DB use karo
app.dependency_overrides[get_db] = override_get_db


# Fake DB ke andar tables create karo
# Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=test_engine)



@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={"userName": "Akshy@123", "password": "Akfgr@746"})
    login = client.post("/auth/login", json={"userName": "Akshy@123", "password": "Akfgr@746"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}