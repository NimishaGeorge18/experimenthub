import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base
from app.db.deps import get_db

# Use SQLite in memory for tests — fast, isolated, no postgres needed
SQLITE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Override the real get_db with test version
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test, drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    """Register + login, return Authorization headers ready to use"""
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_experiment(client, auth_headers):
    """Create a running experiment ready for use in tests"""
    response = client.post("/experiments/", json={
        "name": "Test Experiment",
        "description": "A test",
        "variants": [
            {"name": "Control", "traffic_split": 0.5},
            {"name": "Treatment", "traffic_split": 0.5}
        ]
    }, headers=auth_headers)
    
    experiment = response.json()
    
    # Set it to running
    client.patch(f"/experiments/{experiment['id']}/status",
        json={"status": "running"},
        headers=auth_headers
    )
    return experiment