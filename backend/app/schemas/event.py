from pydantic import BaseModel
from datetime import datetime

class EventRequest(BaseModel):
    user_id: str        # Company's user ID
    experiment_id: int  # Which experiment
    event_type: str     # "purchase", "signup", "click" — company defines this

class EventResponse(BaseModel):
    id: int
    user_id: str
    experiment_id: int
    variant_id: int
    event_type: str
    recorded_at: datetime

    class Config:
        from_attributes = True