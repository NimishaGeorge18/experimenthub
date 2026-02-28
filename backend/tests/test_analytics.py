def test_analytics_conversion_rate(client, auth_headers, sample_experiment):
    """Conversion rate is calculated correctly"""
    exp_id = sample_experiment["id"]

    # Assign 2 users
    client.post(f"/assignments/{exp_id}", json={"user_id": "user_001"})
    client.post(f"/assignments/{exp_id}", json={"user_id": "user_002"})

    # Only user_001 converts
    client.post("/events/", json={
        "user_id": "user_001",
        "experiment_id": exp_id,
        "event_type": "purchase"
    })

    response = client.get(
        f"/analytics/{exp_id}?event_type=purchase",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["experiment_id"] == exp_id
    assert data["winner"] is not None

    # Find the variant that had conversions
    converting_variant = next(
        r for r in data["results"] if r["conversions"] > 0
    )
    assert converting_variant["conversion_rate"] > 0

def test_analytics_no_events(client, auth_headers, sample_experiment):
    """Analytics works even with zero events"""
    exp_id = sample_experiment["id"]
    response = client.get(
        f"/analytics/{exp_id}?event_type=purchase",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["winner"] is None  # No winner if no conversions