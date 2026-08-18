from sqlalchemy import Date, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class DailyStatistic(Base):
    __tablename__ = "daily_statistics"

    # Дата, за яку зберігається статистика
    date: Mapped[Date] = mapped_column(Date, primary_key=True)
    
    # Агреговані показники
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    total_revenue: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    total_withdrawals: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    new_users_count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"<DailyStatistic(date={self.date}, revenue={self.total_revenue})>"