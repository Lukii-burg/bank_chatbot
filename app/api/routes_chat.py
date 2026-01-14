from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot_service import build_reply
from app.models.chat_log import ChatLog
from app.models.case import Case
from app.models.alert import Alert
from app.models.prediction import Prediction
from app.models.transaction import Transaction

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Gather context if ids provided
    context = {}

    if payload.prediction_id:
        pred = db.query(Prediction).filter(Prediction.id == payload.prediction_id).first()
        if pred:
            context["risk_score"] = pred.risk_score
            context["label"] = pred.label
            tx = db.query(Transaction).filter(Transaction.id == pred.transaction_id).first()
            if tx:
                context["amount"] = tx.amount
                context["channel"] = tx.channel
                context["merchant"] = tx.merchant

    if payload.alert_id and "risk_score" not in context:
        alert = db.query(Alert).filter(Alert.id == payload.alert_id).first()
        if alert:
            pred = db.query(Prediction).filter(Prediction.id == alert.prediction_id).first()
            if pred:
                context["risk_score"] = pred.risk_score
                context["label"] = pred.label

    if payload.case_id:
        c = db.query(Case).filter(Case.id == payload.case_id).first()
        if c:
            context["case_status"] = c.status
            context["priority"] = c.priority

    reply = build_reply(payload.message, context)

    # Save chat log
    log = ChatLog(
        user_id=user.id,
        case_id=payload.case_id,
        alert_id=payload.alert_id,
        prediction_id=payload.prediction_id,
        user_message=payload.message,
        assistant_message=reply,
    )
    db.add(log)
    db.commit()

    return ChatResponse(reply=reply)
