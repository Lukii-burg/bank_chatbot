from datetime import datetime
from sqlalchemy import Float, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), index=True)

    risk_score: Mapped[float] = mapped_column(Float)  # 0.0 to 1.0
    label: Mapped[str] = mapped_column(String(20))    # "fraud" or "legit"
    model_version: Mapped[str] = mapped_column(String(50), default="v1")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    transaction = relationship("Transaction")
