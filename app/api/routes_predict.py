from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.db import crud

from app.schemas.predict import PredictRequest, PredictResponse
from app.services.fraud_service import predict_transaction

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("", response_model=PredictResponse)
def predict(
    payload: PredictRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 1) Save transaction
    tx = crud.create_transaction(
        db,
        customer_id=payload.customer_id,
        amount=payload.amount,
        currency=payload.currency,
        merchant=payload.merchant,
        channel=payload.channel,
        location=payload.location,
    )

    # 2) Predict + decision policy
    try:
        score, label, severity, reasons = predict_transaction(payload.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 3) Save prediction
    pred = crud.create_prediction(
        db,
        transaction_id=tx.id,
        risk_score=score,
        label=label,
        model_version="logreg_v1",
    )


    # 4) Create alert for review/fraud only
    alert_id = None
    if label in {"review", "fraud"}:
        alert = crud.create_alert(
            db,
            prediction_id=pred.id,
            severity=severity,   # "med" or "high"
            status="new"
        )
        alert_id = alert.id

    return PredictResponse(
        transaction_id=tx.id,
        prediction_id=pred.id,
        risk_score=score,
        label=label,
        severity=severity,
        alert_id=alert_id,
        reasons=reasons
    )
