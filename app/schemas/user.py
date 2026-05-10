from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    phone_or_email: str
    password: str
    pin: Optional[str] = None
    pseudo: Optional[str] = None

class UserLogin(BaseModel):
    phone_or_email: str
    password: str

class PinLogin(BaseModel):
    pin: str

class UserResponse(BaseModel):
    id: int
    phone_or_email: str
    pseudo: Optional[str] = None
    role: str
    panic_mode_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
