from datetime import datetime
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    merchant: Mapped[str] = mapped_column(String(120))
    channel: Mapped[str] = mapped_column(String(50))   # e.g., online, atm, pos
    location: Mapped[str] = mapped_column(String(120)) # city/country
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
