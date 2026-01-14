from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.core.deps import get_current_user
from app.models.case import Case
from app.models.case_note import CaseNote
from app.models.alert import Alert
from app.schemas.case import (
    CaseCreateRequest,
    CaseAssignRequest,
    CaseStatusRequest,
    CaseNoteRequest,
)

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("")
def list_cases(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cases = db.query(Case).order_by(Case.id.desc()).limit(50).all()
    return [
        {
            "id": c.id,
            "alert_id": c.alert_id,
            "assigned_to_user_id": c.assigned_to_user_id,
            "status": c.status,
            "priority": c.priority,
            "created_at": c.created_at,
        }
        for c in cases
    ]

@router.post("")
def create_case(payload: CaseCreateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = crud.get_case_by_alert_id(db, payload.alert_id)
    if existing:
        return {"message": "Case already exists", "case_id": existing.id}

    alert = db.query(Alert).filter(Alert.id == payload.alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    c = crud.create_case(db, alert_id=payload.alert_id, priority=payload.priority)
    return {"case_id": c.id, "status": c.status, "priority": c.priority}

@router.patch("/{case_id}/assign")
def assign(case_id: int, payload: CaseAssignRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(Case).filter(Case.id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")

    c = crud.assign_case(db, case_id, payload.assigned_to_user_id)
    return {"case_id": c.id, "assigned_to_user_id": c.assigned_to_user_id}

@router.patch("/{case_id}/status")
def set_status(case_id: int, payload: CaseStatusRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(Case).filter(Case.id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")

    allowed = {"open", "investigating", "resolved", "false_positive"}
    if payload.status not in allowed:
        raise HTTPException(status_code=422, detail=f"Invalid status. Use one of {sorted(allowed)}")

    c = crud.update_case_status(db, case_id, payload.status)
    return {"case_id": c.id, "status": c.status}

@router.post("/{case_id}/notes")
def add_note(case_id: int, payload: CaseNoteRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(Case).filter(Case.id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")

    n = crud.add_case_note(db, case_id, user.id, payload.note)
    return {"note_id": n.id, "case_id": n.case_id, "created_at": n.created_at}

@router.get("/{case_id}/notes")
def list_notes(case_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = (
        db.query(CaseNote)
        .filter(CaseNote.case_id == case_id)
        .order_by(CaseNote.id.desc())
        .all()
    )
    return [
        {"id": n.id, "user_id": n.user_id, "note": n.note, "created_at": n.created_at}
        for n in notes
    ]
