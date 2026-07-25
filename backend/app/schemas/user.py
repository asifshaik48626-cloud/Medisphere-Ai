from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: str
    preferred_language: Optional[str] = "en"

class UserCreate(UserBase):
    password: str  # For simplified token validation locally

class UserResponse(UserBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    username: str  # maps to email or phone
    password: str
