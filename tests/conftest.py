import pytest
from app import app
from app.database import Base, engine
from app.models import User
from fastapi.testclient import TestClient
from sqlalchemy import insert

Base.metadata.drop_all(bind=engine)  # Clear database
Base.metadata.create_all(bind=engine)  # Regenerate database

stmt = (
    insert(User).
    values(
        role="A",
        username='admin',
        password="$2b$12$Gr3bUaIsvDYgKnTzC4xIHuA2KgmTX6jb/IAArzfq/JeIhz8ha41Ci"
    )
)

engine.connect().execute(stmt)

stmt = (
    insert(User).
    values(
        role="U",
        username='user',
        password="$2b$12$Gr3bUaIsvDYgKnTzC4xIHuA2KgmTX6jb/IAArzfq/JeIhz8ha41Ci"
    )
)

engine.connect().execute(stmt)


client = TestClient(app)


@pytest.fixture
def signin_body_user():
    """ returns values for user signin route """

    return dict(
        login="user",
        password="test"
    )


@pytest.fixture
def signin_body_admin():
    """ returns values for admin signin route """

    return dict(
        login="admin",
        password="test"
    )


@pytest.fixture
def signin_admin(signin_body_admin):
    """ signin an admin """

    r = client.post("/authentication/login", json=signin_body_admin)
    return r.json()


@pytest.fixture
def signin_user(signin_body_user):
    """ signin a user """

    r = client.post("/authentication/login", json=signin_body_user)
    return r.json()


@pytest.fixture
def client_auth_admin(signin_admin):
    """ add token in header for admin """
    client.headers.update({"Authorization": signin_admin["token"]})
    return client


@pytest.fixture
def client_auth_user(signin_user):
    """ add token in header for user """
    client.headers.update({"Authorization": signin_user["token"]})
    return client


@pytest.fixture
def get_client():
    return client
