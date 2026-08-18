import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app.core.config import settings

logger = logging.getLogger(__name__)

# Создаем асинхронный движок
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# Фабрика сессий
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Получение сессии БД.
    """

    async with async_session() as session:
        try:
            yield session
            await session.commit()

        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise

        finally:
            await session.close()


async def dispose_engine():
    """
    Корректное закрытие соединений с БД.
    """
    await engine.dispose()