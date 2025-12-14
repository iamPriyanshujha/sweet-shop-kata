# backend/app/schemas/user.py (FINAL CORRECTED VERSION)

from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    # FIX: max_length=72 limit hata diya (agar laga hua tha)
    password: str = Field(..., min_length=6)

class UserRead(UserBase):
    id: int
    is_admin: bool
    
    class Config:
        from_attributes = True 

class Token(BaseModel):
    access_token: str
    token_type: str