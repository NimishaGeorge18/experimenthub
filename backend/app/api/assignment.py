from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.assignment import AssignmentRequest, AssignmentResponse
from app.services.assignment import get_or_create_assignment

router = APIRouter(prefix="/assignments", tags=["Assignments"])

# POST /assignments/{experiment_id}
# This is what the company's app calls when a user shows up
# No JWT needed here — this is called by the company's backend, not the dashboard
@router.post("/{experiment_id}", response_model=AssignmentResponse)
def assign_user(
    experiment_id: int,
    payload: AssignmentRequest,
    db: Session = Depends(get_db)
):
    try:
        assignment = get_or_create_assignment(
            db=db,
            experiment_id=experiment_id,
            user_id=payload.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return AssignmentResponse(
        id=assignment.id,
        user_id=assignment.user_id,
        experiment_id=assignment.experiment_id,
        variant_id=assignment.variant_id,
        variant_name=assignment.variant.name,  # Get name from relationship
        assigned_at=assignment.assigned_at
    )