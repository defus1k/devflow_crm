from sqlalchemy import Column, Integer, Float, DateTime, func
from app.db.base import Base # Або імпорт звідки ти береш свій Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)        # Сума транзакції
    created_at = Column(DateTime, default=func.now()) # Дата запису