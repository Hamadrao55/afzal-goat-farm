from sqlalchemy import Column, Integer, String, Float
from database import Base

class Goat(Base):
    __tablename__ = "goats"
    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(String, unique=True)
    breed = Column(String)
    weight = Column(Float)
    status = Column(String, default="Available")

class Transaction(Base):
    __tablename__ = "finance"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    type = Column(String) # 'Income' or 'Expense'