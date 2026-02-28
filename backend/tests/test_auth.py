def test_register_success(client):
    """New user can register"""
    response = client.post("/auth/register", json={
        "email": "newuser@test.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert "id" in data
    assert "password" not in data  # Password must never be returned

def test_register_duplicate_email(client):
    """Cannot register same email twice"""
    client.post("/auth/register", json={
        "email": "same@test.com",
        "password": "password123"
    })
    response = client.post("/auth/register", json={
        "email": "same@test.com",
        "password": "password123"
    })
    assert response.status_code == 409

def test_login_success(client):
    """Registered user can login and gets a token"""
    client.post("/auth/register", json={
        "email": "login@test.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    """Wrong password returns 401"""
    client.post("/auth/register", json={
        "email": "wrong@test.com",
        "password": "correctpass"
    })
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    """Login with email that doesn't exist returns 401"""
    response = client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "password123"
    })
    assert response.status_code == 401