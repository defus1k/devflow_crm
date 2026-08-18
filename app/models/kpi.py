from sqlalchemy import ForeignKey, Integer, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class KPI(Base):
    __tablename__ = "kpis"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Менеджер, для якого встановлено KPI
    manager_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    
    # Назва показника (наприклад: "closed_orders", "revenue_goal")
    metric_name: Mapped[str] = mapped_column(String(50))
    
    # Ціле значення (скільки треба зробити)
    target_value: Mapped[int] = mapped_column(Integer)
    
    # Поточний прогрес
    current_value: Mapped[int] = mapped_column(Integer, default=0)
    
    # Період (місяць/рік)
    period: Mapped[str] = mapped_column(String(20)) 
    
    created_at: Mapped[Date] = mapped_column(Date, server_default=func.now())

    # Зв'язок
    manager = relationship("User", backref="kpi_records")

    def __repr__(self):
        return f"<KPI(manager={self.manager_id}, metric={self.metric_name}, progress={self.current_value}/{self.target_value})>"