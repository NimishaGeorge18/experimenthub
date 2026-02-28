from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db, get_current_user
from app.models.user import User
from app.models.webhook import Webhook, WebhookDeliveryLog
from app.schemas.webhook import WebhookCreate, WebhookResponse, WebhookDeliveryLogResponse

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

# POST /webhooks/{experiment_id} — register a webhook for an experiment
@router.post("/{experiment_id}", response_model=WebhookResponse, status_code=201)
def register_webhook(
    experiment_id: int,
    payload: WebhookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    webhook = Webhook(
        experiment_id=experiment_id,
        url=payload.url,
        secret=payload.secret
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook

# GET /webhooks/{experiment_id} — list all webhooks for an experiment
@router.get("/{experiment_id}", response_model=List[WebhookResponse])
def list_webhooks(
    experiment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Webhook).filter(
        Webhook.experiment_id == experiment_id
    ).all()

# GET /webhooks/{experiment_id}/logs — see delivery history
@router.get("/{experiment_id}/logs", response_model=List[WebhookDeliveryLogResponse])
def get_delivery_logs(
    experiment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WebhookDeliveryLog).join(Webhook).filter(
        Webhook.experiment_id == experiment_id
    ).order_by(WebhookDeliveryLog.attempted_at.desc()).all()