from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.deps import get_db              # DB session
from app.models.user import User            # SQLAlchemy model
from app.schemas.user import UserCreate, UserResponse  # Pydantic schemas

# APIRouter is like a mini FastAPI app — gets registered in main.py
router = APIRouter(prefix="/users", tags=["Users"])

# POST /users — create a new user
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(email=user.email)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists.")
    db.refresh(new_user)    # Reload from DB to get the generated ID
    return new_user

# GET /users — list all users
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id.desc()).limit(50).all()