from sqlalchemy.orm import Session
from app.models.experiment import Experiment
from app.models.assignment import Assignment
from app.models.event import Event
from app.schemas.analytics import AnalyticsResponse, VariantResult

def get_experiment_analytics(
    db: Session,
    experiment_id: int,
    event_type: str
) -> AnalyticsResponse:
    """
    Calculate conversion rates for each variant in an experiment.
    
    Steps:
    1. Get the experiment + its variants
    2. For each variant, count how many users were assigned
    3. For each variant, count how many of those users triggered event_type
    4. Calculate conversion rate
    5. Determine winner
    """

    # Step 1: Get experiment
    experiment = db.query(Experiment).filter(
        Experiment.id == experiment_id
    ).first()

    if not experiment:
        raise ValueError("Experiment not found")

    results = []

    # Step 2 & 3: Loop through each variant and calculate metrics
    for variant in experiment.variants:

        # Count total users assigned to this variant
        total_users = db.query(Assignment).filter(
            Assignment.experiment_id == experiment_id,
            Assignment.variant_id == variant.id
        ).count()

        # Count how many of those users triggered the event
        conversions = db.query(Event).filter(
            Event.experiment_id == experiment_id,
            Event.variant_id == variant.id,
            Event.event_type == event_type   # Only count the specific event
        ).count()

        # Calculate conversion rate — avoid division by zero
        conversion_rate = (conversions / total_users * 100) if total_users > 0 else 0.0

        results.append(VariantResult(
            variant_id=variant.id,
            variant_name=variant.name,
            total_users=total_users,
            conversions=conversions,
            conversion_rate=round(conversion_rate, 2)
        ))

    # Step 4: Find winner — variant with highest conversion rate
    winner = None
    if results:
        best = max(results, key=lambda r: r.conversion_rate)
        # Only declare a winner if at least one conversion happened
        if best.conversions > 0:
            winner = best.variant_name

    return AnalyticsResponse(
        experiment_id=experiment_id,
        experiment_name=experiment.name,
        event_type=event_type,
        results=results,
        winner=winner
    )
