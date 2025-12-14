from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine for the database connection (connect_args is for SQLite only)
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Initializes the database and creates all defined tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency function for FastAPI to get a database session."""
    with Session(engine) as session:
        yield session