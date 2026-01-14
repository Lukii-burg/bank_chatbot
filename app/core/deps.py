from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import crud
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(crud.User).filter(crud.User.id == user_id).first() if hasattr(crud, "User") else None
    # safer way:
    user = crud.get_user_by_id(db, user_id) if hasattr(crud, "get_user_by_id") else None
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user



