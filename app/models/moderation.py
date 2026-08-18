from sqlalchemy import BigInteger, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class UserModeration(Base):
    __tablename__ = "user_moderation"
    __table_args__ = {'extend_existing': True}

    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), primary_key=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    warnings: Mapped[int] = mapped_column(Integer, default=0)
    ban_reason: Mapped[str] = mapped_column(String(255), nullable=True)

    # Зв'язок з користувачем
    user = relationship("app.models.user.User", back_populates="moderation")