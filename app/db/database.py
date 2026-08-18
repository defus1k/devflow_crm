import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    AsyncSession
)
from sqlalchemy.pool import AsyncAdaptedQueuePool
from app.core.config import settings
from app.db.base import Base

# Ініціалізація асинхронного двигуна з налаштуваннями для високо навантажених систем
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=False,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=25,
    max_overflow=10,
    pool_timeout=60,
    pool_recycle=1800,
    pool_pre_ping=True
)

# Фабрика сесій (Session Factory)
# expire_on_commit=False обов'язково для асинхронного режиму
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Залежність (Dependency) для отримання асинхронної сесії БД.
    Використовується в Middleware або сервісах для взаємодії з даними.
    """
    async with async_session_factory() as session:
        try:
            yield session
            # Автоматичний commit транзакції
            await session.commit()
        except Exception as e:
            # Rollback у разі помилки
            await session.rollback()
            logging.error(f"Database error during session: {e}")
            raise
        finally:
            # Закриття з'єднання
            await session.close()

async def init_db():
    """
    Ініціалізація БД (створення таблиць).
    Викликається при запуску бота.
    """
    async with engine.begin() as conn:
        # У продакшн середовищі краще використовувати Alembic, 
        # тому тут ми закоментуємо створення таблиць через метадані, 
        # щоб не було конфліктів з міграціями.
        # await conn.run_sync(Base.metadata.create_all)
        pass

async def close_db():
    """Коректне закриття з'єднань при вимкненні бота."""
    await engine.dispose()