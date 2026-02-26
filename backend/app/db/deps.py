from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.security import decode_access_token

# Tells FastAPI where to expect the token (Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Any route that uses Depends(get_current_user) is protected.
    FastAPI automatically extracts the token from the Authorization header,
    decodes it, finds the user, and passes them to the route.
    If token is missing or invalid, returns 401 automatically.
    """
    from app.models.user import User  # Import here to avoid circular imports

    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user  # This gets injected into the route function