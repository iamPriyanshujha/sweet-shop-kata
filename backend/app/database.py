# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models.base import Base # Assuming your Base declarative model is here
from .models.user import User as UserModel 
from .models.sweet import Sweet as SweetModel
from .core.security import get_password_hash # Needed to hash admin password

# --- Database Configuration ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./sweet_shop.db"

# Create the engine (SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Initialization Functions (Fixing the ImportError) ---

def create_db_and_tables():
    """Create all tables defined in Base metadata."""
    Base.metadata.create_all(bind=engine)

def seed_default_data():
    """Create default admin user and initial sweets if they don't exist."""
    db = SessionLocal()
    
    # 1. Create Admin User
    admin_user = db.query(UserModel).filter(UserModel.username == "admin").first()
    if not admin_user:
        print("Seeding default admin user...")
        # Note: We must ensure the password "adminpass" is <= 72 characters
        hashed_password = get_password_hash("adminpass") 
        
        db_admin = UserModel(
            username="admin", 
            email="admin@sweetshop.com", 
            hashed_password=hashed_password, 
            is_admin=True
        )
        db.add(db_admin)
        db.commit()
        print("Admin user created.")

    # 2. Seed Initial Sweets
    if db.query(SweetModel).count() == 0:
        print("Seeding initial sweets data...")
        sweets_data = [
            {"name": "Gummy Worms", "category": "Gummy", "price": 4.50, "stock": 100},
            {"name": "Chocolate Truffles", "category": "Chocolate", "price": 12.00, "stock": 50},
            {"name": "Lollipop Rainbow", "category": "Hard Candy", "price": 2.25, "stock": 150},
            {"name": "Peppermint Stick", "category": "Mint", "price": 3.00, "stock": 75},
            {"name": "Jelly Beans Mixed", "category": "Gummy", "price": 5.50, "stock": 90},
            {"name": "Caramel Chews", "category": "Chewy", "price": 7.00, "stock": 60},
            {"name": "Marshmallow Fluff", "category": "Soft", "price": 4.00, "stock": 120},
            {"name": "Sour Power Belts", "category": "Sour", "price": 6.75, "stock": 80},
            {"name": "Fudge Brownie Bites", "category": "Chocolate", "price": 9.50, "stock": 40},
            {"name": "Bubblegum Blast", "category": "Gum", "price": 1.50, "stock": 200},
        ]
        
        for data in sweets_data:
            db_sweet = SweetModel(**data)
            db.add(db_sweet)
        
        db.commit()
        print("Sweets data seeded.")
        
    db.close()

# Note: The startup message in main.py will run these functions, 
# resulting in the "Database tables created and seeded with default data." message.