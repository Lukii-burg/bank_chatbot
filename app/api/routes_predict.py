from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.schemas.predict import PredictRequest, PredictResponse
from app.services.fraud_service import (
    simple_risk_score,
    label_from_score,
    severity_from_score,
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("", response_model=PredictResponse)
def predict(
    payload: PredictRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),  # ✅ protect endpoint
):
    tx = crud.create_transaction(
        db,
        customer_id=payload.customer_id,
        amount=payload.amount,
        currency=payload.currency,
        merchant=payload.merchant,
        channel=payload.channel,
        location=payload.location,
    )

    score = simple_risk_score(payload.amount, payload.channel)
    label = label_from_score(score)
    pred = crud.create_prediction(db, transaction_id=tx.id, risk_score=score, label=label)

    alert_id = None
    if label == "fraud":
        sev = severity_from_score(score)
        alert = crud.create_alert(db, prediction_id=pred.id, severity=sev)
        alert_id = alert.id

    return PredictResponse(
        transaction_id=tx.id,
        prediction_id=pred.id,
        risk_score=score,
        label=label,
        alert_id=alert_id,
    )
