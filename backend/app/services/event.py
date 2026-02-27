from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.assignment import Assignment

def record_event(
    db: Session,
    user_id: str,
    experiment_id: int,
    event_type: str
) -> Event:
    # """
    # Record that a user did something (purchase, signup, click).
    # We look up which variant they were assigned to,
    # then store the event linked to that variant.
    # """

    # Find which variant this user was assigned to
    assignment = db.query(Assignment).filter(
        Assignment.user_id == user_id,
        Assignment.experiment_id == experiment_id
    ).first()

    if not assignment:
        raise ValueError(
            f"User '{user_id}' has no assignment for experiment {experiment_id}. "
            "They must be assigned before events can be recorded."
        )

    # Record the event
    event = Event(
        user_id=user_id,
        experiment_id=experiment_id,
        variant_id=assignment.variant_id,  # Link to their variant
        event_type=event_type
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event