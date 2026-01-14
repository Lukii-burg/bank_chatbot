from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class PredictRequest(BaseModel):
    customer_id: str
    amount: float
    currency: str = "USD"
    merchant: str
    channel: str
    location: str

class PredictResponse(BaseModel):
    transaction_id: int
    prediction_id: int
    risk_score: float = Field(..., ge=0.0, le=1.0)
    label: str           # legit / review / fraud
    severity: str        # none / med / high
    alert_id: Optional[int] = None
    reasons: List[Dict] = []
