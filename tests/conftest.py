import pytest
from fastapi.testclient import TestClient

from app.dependencies.database import get_db
from app.main import app
from tests.auth import auth_headers
from tests.database import Base, engine, override_get_db

# ---------------------------------------------------------
# Override FastAPI dependency
# ---------------------------------------------------------

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """
    Returns a clean TestClient for every test.
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def authenticated_headers(client):
    """
    Returns JWT authentication headers for a test user.
    """
    return auth_headers(client)
