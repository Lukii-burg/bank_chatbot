from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    case_id: int | None = None
    alert_id: int | None = None
    prediction_id: int | None = None

class ChatResponse(BaseModel):
    reply: str
