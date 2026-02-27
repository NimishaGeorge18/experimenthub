from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics import get_experiment_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# GET /analytics/{experiment_id}?event_type=purchase
@router.get("/{experiment_id}", response_model=AnalyticsResponse)
def get_analytics(
    experiment_id: int,
    event_type: str = Query(..., description="Event to measure e.g. purchase, signup, click"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Protected — only admins
):
    try:
        return get_experiment_analytics(
            db=db,
            experiment_id=experiment_id,
            event_type=event_type
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))