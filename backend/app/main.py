# backend/app/main.py (FINAL COMPLETE VERSION)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables, seed_default_data
from .api.auth import router as auth_router
from .api.sweets import router as sweets_router # Ensure this import is correct

app = FastAPI(title="Sweet Shop API")

# --- CORS Configuration ---
# Allows your frontend (running on localhost:5173) to communicate with the backend
origins = [
    "http://localhost:5173", # Your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Include Routers ---
app.include_router(auth_router, prefix="/api/auth")   # Handles /api/auth/register and /api/auth/login
app.include_router(sweets_router, prefix="/api/sweets") # Handles /api/sweets/...


# --- Startup Event ---
@app.on_event("startup")
def on_startup():
    """Initializes database tables and seeds default data (like the admin user)."""
    create_db_and_tables()
    seed_default_data()


# --- Root Endpoint (Optional Check) ---
@app.get("/")
def read_root():
    return {"message": "Sweet Shop API is running"}