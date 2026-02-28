from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db, get_current_user
from app.models.user import User
from app.models.experiment import Experiment, Variant
from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentStatusUpdate
)
from app.webhooks.sender import send_webhook 

router = APIRouter(prefix="/experiments", tags=["Experiments"])

# POST /experiments — create a new experiment (protected)
@router.post("/", response_model=ExperimentResponse, status_code=201)
def create_experiment(
    payload: ExperimentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Must be logged in
):
    # Create the experiment
    experiment = Experiment(
        name=payload.name,
        description=payload.description,
        created_by=current_user.id  # Track who created it
    )
    db.add(experiment)
    db.flush()  # Gets the experiment.id without committing yet

    # Create all variants linked to this experiment
    for v in payload.variants:
        variant = Variant(
            experiment_id=experiment.id,
            name=v.name,
            description=v.description,
            traffic_split=v.traffic_split
        )
        db.add(variant)

    db.commit()
    db.refresh(experiment)
    return experiment

# GET /experiments — list all experiments (protected)
@router.get("/", response_model=List[ExperimentResponse])
def list_experiments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Experiment).order_by(Experiment.id.desc()).all()

# GET /experiments/{id} — get one experiment (protected)
@router.get("/{experiment_id}", response_model=ExperimentResponse)
def get_experiment(
    experiment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found.")
    return experiment

# PATCH /experiments/{id}/status — start, pause, or complete an experiment
@router.patch("/{experiment_id}/status", response_model=ExperimentResponse)
def update_status(
    experiment_id: int,
    payload: ExperimentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found.")
    
    experiment.status = payload.status
    db.commit()
    db.refresh(experiment)

    # Fire webhook notification after status change
    send_webhook(
        db=db,
        experiment_id=experiment_id,
        event_type="experiment.status_changed",
        payload={
            "event": "experiment.status_changed",
            "experiment_id": experiment_id,
            "experiment_name": experiment.name,
            "new_status": payload.status.value
        }
    )

    return experiment
