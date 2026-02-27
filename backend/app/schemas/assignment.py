from pydantic import BaseModel
from datetime import datetime

class AssignmentRequest(BaseModel):
    user_id: str   # The company sends their user's ID

class AssignmentResponse(BaseModel):
    id: int
    user_id: str
    experiment_id: int
    variant_id: int
    variant_name: str
    assigned_at: datetime

    class Config:
        from_attributes = True