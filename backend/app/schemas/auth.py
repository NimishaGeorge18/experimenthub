from pydantic import BaseModel, EmailStr

# What register + login endpoints accept
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# What login returns
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Standard OAuth2 convention

# What gets returned about the logged-in user
class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True