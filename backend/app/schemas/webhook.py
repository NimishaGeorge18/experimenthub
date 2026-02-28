from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class WebhookCreate(BaseModel):
    url: str              # Company's URL to receive notifications
    secret: Optional[str] = None  # Optional secret key

class WebhookResponse(BaseModel):
    id: int
    experiment_id: int
    url: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class WebhookDeliveryLogResponse(BaseModel):
    id: int
    webhook_id: int
    event_type: str
    payload: str
    response_status: Optional[int]
    success: bool
    attempted_at: datetime

    class Config:
        from_attributes = True