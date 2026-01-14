from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
def list_alerts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    alerts = db.query(Alert).order_by(Alert.id.desc()).limit(50).all()
    return [
        {
            "id": a.id,
            "prediction_id": a.prediction_id,
            "severity": a.severity,
            "status": a.status,
            "created_at": a.created_at,
        }
        for a in alerts
    ]
