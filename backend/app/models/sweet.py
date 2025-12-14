# backend/app/models/sweet.py

from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class Sweet(Base):
    __tablename__ = "sweets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)