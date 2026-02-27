from pydantic import BaseModel
from typing import List, Optional

class VariantResult(BaseModel):
    variant_id: int
    variant_name: str
    total_users: int        # How many users were assigned to this variant
    conversions: int        # How many triggered the event_type we're measuring
    conversion_rate: float  # conversions / total_users * 100

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    experiment_id: int
    experiment_name: str
    event_type: str
    results: List[VariantResult]
    winner: Optional[str] = None  # Variant name with highest conversion rate
    