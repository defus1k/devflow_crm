from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole
from typing import Optional, List

class UserRepository:
    """
    Репозиторій для роботи з користувачами.
    Інкапсулює всю логіку запитів до таблиці 'users'.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Отримати користувача за його ID в Telegram."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int, username: Optional[str], full_name: Optional[str], role: UserRole = UserRole.CLIENT) -> User:
        """Створити нового користувача в системі."""
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            role=role
        )
        self.session.add(user)
        await self.session.flush()  # Зберігаємо в пам'яті до коміту
        return user

    async def update_role(self, telegram_id: int, new_role: UserRole) -> bool:
        """Оновити роль користувача (наприклад, при наймі на роботу)."""
        result = await self.session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(role=new_role)
        )
        return result.rowcount > 0

    async def get_all_by_role(self, role: UserRole) -> List[User]:
        """Отримати список всіх менеджерів або розробників."""
        result = await self.session.execute(
            select(User).where(User.role == role)
        )
        return list(result.scalars().all())

    async def update_balance(self, telegram_id: int, amount: float) -> bool:
        """Зміна балансу працівника (виплата)."""
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.balance += amount
            return True
        return False