from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.user import User
from app.models.transaction import Transaction
from app.models.prediction import Prediction
from app.models.alert import Alert
from app.models.case import Case
from app.models.case_note import CaseNote



def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()

def create_role(db: Session, name: str) -> Role:
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, full_name: str, email: str, password_hash: str, role_id: int) -> User:
    user = User(full_name=full_name, email=email, password_hash=password_hash, role_id=role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_transaction(db: Session, **kwargs) -> Transaction:
    tx = Transaction(**kwargs)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def create_prediction(db: Session, transaction_id: int, risk_score: float, label: str, model_version: str = "v1") -> Prediction:
    p = Prediction(transaction_id=transaction_id, risk_score=risk_score, label=label, model_version=model_version)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def create_alert(db: Session, prediction_id: int, severity: str, status: str = "new") -> Alert:
    a = Alert(prediction_id=prediction_id, severity=severity, status=status)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_case_by_alert_id(db: Session, alert_id: int):
    return db.query(Case).filter(Case.alert_id == alert_id).first()

def create_case(db: Session, alert_id: int, priority: str = "med"):
    c = Case(alert_id=alert_id, priority=priority)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def assign_case(db: Session, case_id: int, user_id: int):
    c = db.query(Case).filter(Case.id == case_id).first()
    c.assigned_to_user_id = user_id
    db.commit()
    db.refresh(c)
    return c

def update_case_status(db: Session, case_id: int, status: str):
    c = db.query(Case).filter(Case.id == case_id).first()
    c.status = status
    db.commit()
    db.refresh(c)
    return c

def add_case_note(db: Session, case_id: int, user_id: int, note: str):
    n = CaseNote(case_id=case_id, user_id=user_id, note=note)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n
