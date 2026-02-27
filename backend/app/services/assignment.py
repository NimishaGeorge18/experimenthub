import random
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.models.experiment import Experiment, ExperimentStatus

def get_or_create_assignment(
    db: Session,
    experiment_id: int,
    user_id: str
) -> Assignment:
    """
    Core A/B logic:
    1. Check if this user already has an assignment for this experiment
    2. If yes → return the same one (consistency)
    3. If no  → randomly pick a variant based on traffic split
    """

    # Step 1: Check if already assigned
    existing = db.query(Assignment).filter(
        Assignment.experiment_id == experiment_id,
        Assignment.user_id == user_id
    ).first()

    if existing:
        return existing  # Always return the same variant

    # Step 2: Get the experiment and make sure it's running
    experiment = db.query(Experiment).filter(
        Experiment.id == experiment_id
    ).first()

    if not experiment:
        raise ValueError("Experiment not found")

    if experiment.status != ExperimentStatus.running:
        raise ValueError("Experiment is not running")

    # Step 3: Randomly pick a variant based on traffic split
    # Example: Control=0.5, Treatment=0.5
    # random.random() gives a number between 0 and 1
    # We walk through variants accumulating weight until we exceed the random number
    variants = experiment.variants
    roll = random.random()  # e.g. 0.73
    
    cumulative = 0.0
    selected_variant = variants[-1]  # fallback to last variant
    
    for variant in variants:
        cumulative += variant.traffic_split
        if roll < cumulative:
            selected_variant = variant
            break

    # Step 4: Save the assignment
    assignment = Assignment(
        user_id=user_id,
        experiment_id=experiment_id,
        variant_id=selected_variant.id
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
