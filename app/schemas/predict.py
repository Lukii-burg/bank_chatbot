from pydantic import BaseModel

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
    risk_score: float
    label: str
    alert_id: int | None = None
