from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    url = Column(String, nullable=False)          # Company's endpoint URL
    secret = Column(String, nullable=True)        # Optional secret for verification
    is_active = Column(Boolean, default=True)     # Can be disabled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    experiment = relationship("Experiment")
    delivery_logs = relationship("WebhookDeliveryLog", back_populates="webhook")

class WebhookDeliveryLog(Base):
    __tablename__ = "webhook_delivery_logs"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False)
    event_type = Column(String, nullable=False)    # "experiment.status_changed"
    payload = Column(String, nullable=False)       # JSON string of what we sent
    response_status = Column(Integer, nullable=True)  # HTTP status we got back
    success = Column(Boolean, nullable=False)      # True if 2xx response
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    webhook = relationship("Webhook", back_populates="delivery_logs")