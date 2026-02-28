import httpx
import json
from sqlalchemy.orm import Session
from app.models.webhook import Webhook, WebhookDeliveryLog

def send_webhook(
    db: Session,
    experiment_id: int,
    event_type: str,
    payload: dict
):
    """
    Find all active webhooks for this experiment and send them.
    Logs every attempt whether it succeeds or fails.
    """

    # Get all active webhooks for this experiment
    webhooks = db.query(Webhook).filter(
        Webhook.experiment_id == experiment_id,
        Webhook.is_active == True
    ).all()

    if not webhooks:
        return  # No webhooks registered, nothing to do

    payload_str = json.dumps(payload)  # Convert dict to JSON string for sending + logging

    for webhook in webhooks:
        success = False
        response_status = None

        try:
            # Send HTTP POST to company's URL
            # timeout=5 means give up after 5 seconds
            response = httpx.post(
                webhook.url,
                json=payload,
                timeout=5.0,
                headers={"Content-Type": "application/json"}
            )
            response_status = response.status_code
            success = response.status_code < 400  # 2xx and 3xx = success

        except Exception as e:
            # Network error, timeout, invalid URL etc.
            success = False
            response_status = None

        # Always log the attempt regardless of success or failure
        log = WebhookDeliveryLog(
            webhook_id=webhook.id,
            event_type=event_type,
            payload=payload_str,
            response_status=response_status,
            success=success
        )
        db.add(log)

    db.commit()