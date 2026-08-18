from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
    DateTime,
    func,
    Text,
    Numeric,
    Integer, # Додано імпорт Integer
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Telegram ID клиента
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id")
    )

    # Тип проекта
    project_type: Mapped[str] = mapped_column(String(50))

    # Название
    title: Mapped[str] = mapped_column(String(255))

    # Описание
    description: Mapped[str] = mapped_column(Text)

    # Бюджет
    budget: Mapped[float] = mapped_column(Numeric(10, 2))

    # Контакт (делаем НЕ обязательным)
    contact: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None
    )

    # ID гілки форуму (Додано поле)
    thread_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=None
    )

    # Менеджер
    manager_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    # Разработчик
    developer_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    # Статус
    status: Mapped[str] = mapped_column(
        String(50),
        default="new"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", backref="orders")

    def __repr__(self):
        return f"<Order #{self.id}>"