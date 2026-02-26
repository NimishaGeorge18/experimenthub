from pydantic import BaseModel, EmailStr

# What the API accepts when creating a user (input)
class UserCreate(BaseModel):
    email: EmailStr        # EmailStr validates it's a real email format

# What the API sends back (output) — notice no password here
class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True  # Lets Pydantic read SQLAlchemy model objects