# backend/app/api/auth.py (FINAL CORRECTED VERSION)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Imports from your project structure
from ..database import get_db
from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserRead
from ..schemas.token import Token
from ..core.security import (
    authenticate_user,
    create_access_token, 
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    tags=["Auth"]
)

# --- 1. USER REGISTRATION ENDPOINT ---
# FIX: Changed path from "/auth/register" to "/register"
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate, # Expects username, password, email
    db: Session = Depends(get_db)
):
    """Register a new user, checking for existing username/email."""
    
    # Check if username already exists
    if db.query(UserModel).filter(UserModel.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    if user_in.email and db.query(UserModel).filter(UserModel.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # Hash the password
    hashed_password = get_password_hash(user_in.password)
    
    # Create the new user object
    db_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        # Default user is NOT admin
        is_admin=False 
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


# --- 2. USER LOGIN ENDPOINT ---
# FIX: Changed path from "/auth/login" to "/login"
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return a JWT access token."""
    
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create token, passing the admin status
    access_token = create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}