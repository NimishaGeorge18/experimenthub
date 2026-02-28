def test_assign_user(client, sample_experiment):
    """User gets assigned to a variant"""
    exp_id = sample_experiment["id"]
    response = client.post(f"/assignments/{exp_id}", json={
        "user_id": "user_001"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_001"
    assert data["variant_id"] in [v["id"] for v in sample_experiment["variants"]]

def test_assignment_consistency(client, sample_experiment):
    """Same user always gets same variant"""
    exp_id = sample_experiment["id"]
    
    first = client.post(f"/assignments/{exp_id}", json={"user_id": "user_001"})
    second = client.post(f"/assignments/{exp_id}", json={"user_id": "user_001"})
    
    assert first.json()["variant_id"] == second.json()["variant_id"]
    assert first.json()["id"] == second.json()["id"]  # Same assignment record

def test_assign_to_non_running_experiment(client, auth_headers):
    """Cannot assign user to draft experiment"""
    create = client.post("/experiments/", json={
        "name": "Draft Exp",
        "variants": [
            {"name": "A", "traffic_split": 0.5},
            {"name": "B", "traffic_split": 0.5}
        ]
    }, headers=auth_headers)
    exp_id = create.json()["id"]  # Status is draft

    response = client.post(f"/assignments/{exp_id}", json={"user_id": "user_001"})
    assert response.status_code == 400