from pydantic import BaseModel, field_validator
from typing import List, Optional
from app.models.experiment import ExperimentStatus

# --- Variant Schemas ---

class VariantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    traffic_split: float

class VariantResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    traffic_split: float

    class Config:
        from_attributes = True

# --- Experiment Schemas ---

class ExperimentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    variants: List[VariantCreate]  # Must provide variants when creating experiment

    # Validate that traffic splits add up to 1.0 (100%)
    @field_validator("variants")
    @classmethod
    def validate_traffic_split(cls, variants):
        total = sum(v.traffic_split for v in variants)
        if not (0.99 <= total <= 1.01):  # Allow tiny floating point errors
            raise ValueError(f"Traffic splits must add up to 1.0, got {total}")
        if len(variants) < 2:
            raise ValueError("An experiment must have at least 2 variants")
        return variants

class ExperimentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: ExperimentStatus
    created_by: int
    variants: List[VariantResponse]

    class Config:
        from_attributes = True

class ExperimentStatusUpdate(BaseModel):
    status: ExperimentStatus  # Used to start/pause/complete an experiment