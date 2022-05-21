from datetime import timedelta

import pytest
from sqlmodel import Session, create_engine
from starlette.testclient import TestClient

from app.database import services as database_services
from app.database.deps import get_session
from app.main import app
from app.settings import settings
from app.users import services as users_services
from app.users.schemas import User

engine = create_engine(settings.test_database_url)


@pytest.fixture(scope="session")
def session() -> Session:
    """Clear test database and yield test session"""

    database_services.drop_tables(engine)
    database_services.create_tables(engine)

    try:
        with Session(engine) as session:
            yield session
    finally:
        database_services.drop_tables(engine)


@pytest.fixture(autouse=True)
def session_rollback(session: Session):
    """Rollback session after each test"""
    yield
    session.rollback()


@pytest.fixture
def anonymous_client(session: Session) -> TestClient:
    """Yield test client with overridden get_session deps"""

    app.dependency_overrides[get_session] = lambda: session

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides[get_session] = get_session


@pytest.fixture
def client(anonymous_client: TestClient, user: User) -> TestClient:
    """Return authorized test client"""

    client = TestClient(anonymous_client.app)
    token = users_services.encode_jwt_token(user.id, timedelta(days=1))
    client.headers.setdefault("Authorization", f"Bearer {token}")

    return client
