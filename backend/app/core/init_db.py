from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User

def init_db(db: Session) -> None:
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        user = User(
            username="admin",
            hashed_password=get_password_hash("admin"),
            is_superuser=True
        )
        db.add(user)
        db.commit()
        db.refresh(user) 