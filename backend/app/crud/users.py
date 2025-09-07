from sqlalchemy.orm import Session
from ..models import User

def get_user_by_email(db: Session, user_email: int) -> User:
    return db.query(User).filter(User.email == user_email).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, password_hash: str):
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user, password_hash: str):
    user.password_hash = password_hash
    db.commit()
    db.refresh(user)
    return user