from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.event import EventRequest, EventResponse
from app.services.event import record_event

router = APIRouter(prefix="/events", tags=["Events"])

# POST /events — company calls this when a user does something
@router.post("/", response_model=EventResponse, status_code=201)
def track_event(
    payload: EventRequest,
    db: Session = Depends(get_db)
):
    try:
        event = record_event(
            db=db,
            user_id=payload.user_id,
            experiment_id=payload.experiment_id,
            event_type=payload.event_type
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return event