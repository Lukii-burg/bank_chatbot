from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    prediction_id: Mapped[int] = mapped_column(ForeignKey("predictions.id"), index=True)

    severity: Mapped[str] = mapped_column(String(10), default="low")   # low/med/high
    status: Mapped[str] = mapped_column(String(20), default="new")     # new/seen/closed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    prediction = relationship("Prediction")
