from pydantic import BaseModel

class CaseCreateRequest(BaseModel):
    alert_id: int
    priority: str = "med"

class CaseAssignRequest(BaseModel):
    assigned_to_user_id: int

class CaseStatusRequest(BaseModel):
    status: str  # open/investigating/resolved/false_positive

class CaseNoteRequest(BaseModel):
    note: str
