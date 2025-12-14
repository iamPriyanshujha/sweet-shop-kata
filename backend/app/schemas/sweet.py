# backend/app/schemas/sweet.py (ADD THIS NEW CLASS)

from pydantic import BaseModel, Field

# Existing Schemas
class SweetBase(BaseModel):
    name: str
    category: str
    price: float = Field(..., gt=0)
    quantity: int = Field(0, ge=0)

class SweetCreate(SweetBase):
    pass

class SweetRead(SweetBase):
    id: int

    class Config:
        from_attributes = True

# --- NEW: Purchase Schema ---
class SweetPurchase(BaseModel):
    quantity: int = Field(..., gt=0, description="The number of units to purchase.")
# ---------------------------