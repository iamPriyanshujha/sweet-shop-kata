from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# --- Sweet Models ---

class SweetBase(SQLModel):
    name: str = Field(index=True)
    category: str
    price: float
    quantity: int = Field(default=0, ge=0) # ge=0 ensures quantity is non-negative

class Sweet(SweetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class SweetRead(SweetBase):
    id: int

class SweetCreate(SweetBase):
    pass 

class SweetUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

# --- User Models ---

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

# backend/app/db/models.py
# ... (existing code for User, UserCreate, etc.)

from sqlmodel import SQLModel, Field # <-- Make sure you import SQLModel and Field or BaseModel

# ... existing User classes ...

# New class for the Login Response Body
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Optional, but often included for the token payload (data inside the JWT)
class TokenPayload(SQLModel):
    sub: str | None = None # Subject is usually the username