# backend/app/api/sweets.py (FINAL FIX: Indentation and Prefix)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Use direct relative imports
from ..database import get_db
from ..models.sweet import Sweet as SweetModel
from ..schemas.sweet import SweetRead, SweetCreate, SweetPurchase
from ..core.security import get_current_user

# FIX: Removed prefix="/sweets" to stop the 404 double prefixing error
router = APIRouter(
    tags=["Sweets"]
)

# Dependency to check for Admin status (Indentation must be correct here)
def check_admin_permission(current_user: dict = Depends(get_current_user)):
    """Raises 403 Forbidden if the current user is not marked as an admin."""
    # --- INDENTATION START ---
    if not current_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires administrative privileges"
        )
    return current_user
    # --- INDENTATION END ---


# GET /api/sweets - Fetches all sweets (Now maps correctly to /api/sweets/)
@router.get("/", response_model=List[SweetRead])
async def read_sweets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Login required
):
    """Fetches all sweets currently in the inventory."""
    sweets = db.query(SweetModel).all()
    return sweets

# POST /api/sweets - Creates a new sweet (Requires admin)
@router.post("/", response_model=SweetRead, status_code=status.HTTP_201_CREATED)
async def create_sweet(
    sweet_in: SweetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(check_admin_permission)
):
    """Adds a new sweet to the inventory (Admin only)."""

    existing_sweet = db.query(SweetModel).filter(SweetModel.name == sweet_in.name).first()
    if existing_sweet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A sweet with this name already exists."
        )

    db_sweet = SweetModel(**sweet_in.model_dump())

    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)

    return db_sweet

# --- Purchase Endpoint ---
@router.post("/{sweet_id}/purchase", status_code=status.HTTP_200_OK)
async def purchase_sweet(
    sweet_id: int,
    purchase_data: SweetPurchase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Allows a logged-in user to purchase a specified quantity of a sweet."""
    
    db_sweet = db.query(SweetModel).filter(SweetModel.id == sweet_id).first()
    
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    requested_quantity = purchase_data.quantity
    
    if requested_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero"
        )
        
    if db_sweet.stock < requested_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {db_sweet.stock} available."
        )
        
    db_sweet.stock -= requested_quantity
    db.commit()
    db.refresh(db_sweet)
    
    total_price = db_sweet.price * requested_quantity
    
    return {
        "message": f"Successfully purchased {requested_quantity} units of {db_sweet.name}.",
        "new_stock": db_sweet.stock,
        "total_price": total_price,
        "sweet_id": db_sweet.id
    }