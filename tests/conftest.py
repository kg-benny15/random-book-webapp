"""
Pytest configuration for FastAPI testing.

Fixtures:
- setup_database: Creates/drops tables once per test session
- db_session: Provides database session for each test
- client: HTTP client with dependency override
"""

import pytest
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, ReadingMaterial
from app.core.database import test_engine, get_session
from app.core.security import hash_password

# ============================================================
# DATABASE SETUP (Session-scoped)
# ============================================================


@pytest.fixture(scope="session")
def setup_database():
    """
    Create all tables before tests, drop them after.
    Runs once per test session (not per test).
    """
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


# ============================================================
# DATABASE SESSION (Function-scoped)
# ============================================================


@pytest.fixture()
def db_session(setup_database):
    """
    Provide a database session for each test.
    Depends on setup_database (tables exist before session).
    Uses get_session(testing=True) which includes rollback.
    """
    session_generator = get_session(testing=True)
    session = next(session_generator)

    yield session
    # Cerrar el generador correctamente
    try:
        next(session_generator)  # Esto ejecuta el finally en get_session
    except StopIteration:
        pass


# ============================================================
# HTTP CLIENT (Function-scoped)
# ============================================================


@pytest.fixture()
def client(db_session):
    """
    Provide TestClient with database dependency overridden.
    All API calls use the test database session.
    """

    def override_get_session():
        """Replace real DB session with test session."""
        yield db_session

    # Override FastAPI dependency
    app.dependency_overrides[get_session] = override_get_session

    # Create test client
    with TestClient(app) as test_client:
        yield test_client

    # Clean up after test
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db_session):
    test_user = User(
        username="test_user",
        email="test@email.com",
        hash_password=hash_password("password"),
    )

    db_session.add(test_user)
    db_session.flush()
    db_session.refresh(test_user)

    return test_user


@pytest.fixture()
def test_reading_material(db_session):
    test_reading_material = ReadingMaterial(
        work_id="test_workid",
        title="Test Title",
        author="Test Author",
        total_pages=25,
        material_type="book",
    )

    db_session.add(test_reading_material)
    db_session.flush()
    db_session.refresh(test_reading_material)

    return test_reading_material
