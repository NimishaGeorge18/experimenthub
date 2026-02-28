def test_record_event(client, sample_experiment):
    """Can record event for assigned user"""
    exp_id = sample_experiment["id"]

    # First assign the user
    client.post(f"/assignments/{exp_id}", json={"user_id": "user_001"})

    # Then record event
    response = client.post("/events/", json={
        "user_id": "user_001",
        "experiment_id": exp_id,
        "event_type": "purchase"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "purchase"
    assert data["user_id"] == "user_001"

def test_event_without_assignment(client, sample_experiment):
    """Cannot record event for user with no assignment"""
    response = client.post("/events/", json={
        "user_id": "unassigned_user",
        "experiment_id": sample_experiment["id"],
        "event_type": "purchase"
    })
    assert response.status_code == 400