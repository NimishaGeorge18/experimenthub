import enum
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Experiment can only be in one of these states
class ExperimentStatus(str, enum.Enum):
    draft = "draft"         # Created but not running yet
    running = "running"     # Actively assigning users
    paused = "paused"       # Temporarily stopped
    completed = "completed" # Done, winner decided

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)                    # "Checkout Button Test"
    description = Column(String, nullable=True)              # Optional notes
    status = Column(Enum(ExperimentStatus), default=ExperimentStatus.draft, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Which admin created it
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships — lets you do experiment.variants to get all variants
    variants = relationship("Variant", back_populates="experiment", cascade="all, delete")
    creator = relationship("User", backref="experiments")

class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    name = Column(String, nullable=False)          # "Control" or "Treatment"
    description = Column(String, nullable=True)    # "Old green button" / "New red button"
    traffic_split = Column(Float, nullable=False)  # 0.5 = 50% of traffic

    # Relationship back to experiment
    experiment = relationship("Experiment", back_populates="variants")