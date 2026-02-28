def test_create_experiment(client, auth_headers):
    """Admin can create an experiment with variants"""
    response = client.post("/experiments/", json={
        "name": "Button Color Test",
        "description": "Red vs Blue",
        "variants": [
            {"name": "Control", "traffic_split": 0.5},
            {"name": "Treatment", "traffic_split": 0.5}
        ]
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Button Color Test"
    assert data["status"] == "draft"
    assert len(data["variants"]) == 2

def test_create_experiment_invalid_split(client, auth_headers):
    """Traffic splits must add up to 1.0"""
    response = client.post("/experiments/", json={
        "name": "Bad Split Test",
        "variants": [
            {"name": "Control", "traffic_split": 0.4},
            {"name": "Treatment", "traffic_split": 0.4}  # Only 80% total
        ]
    }, headers=auth_headers)
    assert response.status_code == 422  # Validation error

def test_create_experiment_requires_auth(client):
    """Cannot create experiment without token"""
    response = client.post("/experiments/", json={
        "name": "Unauthorized",
        "variants": [
            {"name": "A", "traffic_split": 0.5},
            {"name": "B", "traffic_split": 0.5}
        ]
    })
    assert response.status_code == 401

def test_list_experiments(client, auth_headers):
    """Can list all experiments"""
    client.post("/experiments/", json={
        "name": "Exp 1",
        "variants": [
            {"name": "A", "traffic_split": 0.5},
            {"name": "B", "traffic_split": 0.5}
        ]
    }, headers=auth_headers)
    response = client.get("/experiments/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_update_experiment_status(client, auth_headers):
    """Can change experiment status"""
    create = client.post("/experiments/", json={
        "name": "Status Test",
        "variants": [
            {"name": "A", "traffic_split": 0.5},
            {"name": "B", "traffic_split": 0.5}
        ]
    }, headers=auth_headers)
    exp_id = create.json()["id"]

    response = client.patch(f"/experiments/{exp_id}/status",
        json={"status": "running"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "running"