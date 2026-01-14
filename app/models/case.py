from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)

    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"), index=True, unique=True)
    assigned_to_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    status: Mapped[str] = mapped_column(String(30), default="open")  # open/investigating/resolved/false_positive
    priority: Mapped[str] = mapped_column(String(10), default="med") # low/med/high

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert")
    assigned_to = relationship("User")
