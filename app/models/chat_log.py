from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Text, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    # optional context links
    case_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    alert_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prediction_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user_message: Mapped[str] = mapped_column(Text)
    assistant_message: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    model: Mapped[str] = mapped_column(String(50), default="rule_based_v1")
