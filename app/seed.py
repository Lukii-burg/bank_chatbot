from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db import crud
from app.core.security import hash_password

ROLES = ["admin", "teller", "analyst", "manager"]

def seed():
    db: Session = SessionLocal()
    try:
        # Roles
        for r in ROLES:
            if not crud.get_role_by_name(db, r):
                crud.create_role(db, r)

        # Admin user (dev default)
        admin_email = "admin@bank.com"
        admin = crud.get_user_by_email(db, admin_email)
        if not admin:
            admin_role = crud.get_role_by_name(db, "admin")
            crud.create_user(
                db,
                full_name="System Admin",
                email=admin_email,
                password_hash=hash_password("Admin123!"),
                role_id=admin_role.id,
            )
            print("✅ Seeded roles + admin user")
            print("Login: admin@bank.com / Admin123!")
        else:
            print("✅ Admin already exists, seed skipped")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
