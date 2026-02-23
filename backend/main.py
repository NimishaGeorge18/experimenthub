from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.database import Base, engine, SessionLocal
from app.models.user import User
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request schema
class UserCreate(BaseModel):
    email: str

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user