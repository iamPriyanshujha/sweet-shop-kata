# backend/app/core/security.py (FINAL FIX - HASHING SCHEME CHANGE)

from typing import Optional, Union, Dict
from sqlalchemy.orm import Session
from ..models.user import User as UserModel 
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configuration
SECRET_KEY = "YOUR_SUPER_SECRET_KEY" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# FIX: 'bcrypt' se 'sha256_crypt' kiya taaki length error khatam ho jaaye
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto") 

# OAuth2PasswordBearer is used to extract the token from the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login") 


# --- Password Hashing/Verification ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Uses sha256_crypt which handles long passwords without error."""
    return pwd_context.hash(password)


# --- Authentication & Token Functions ---
def authenticate_user(db: Session, username: str, password: str) -> Optional[UserModel]:
    """Attempts to authenticate a user by username and password against the database."""
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Dependency for Protected Routes ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(lambda: next(get_db_session()))):
    """Decodes the JWT token and returns the user payload (username, is_admin)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)

        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    return {"username": username, "is_admin": is_admin}


# --- Helper function to resolve the database dependency issue inside get_current_user ---
def get_db_session():
    # Fix for circular import
    from ..database import SessionLocal 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()