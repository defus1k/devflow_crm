from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session # Ми припускаємо, що у вас є цей DI провайдер
from app.core.logger import logger

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_session)):
    """
    Перевірка стану системи:
    1. Перевіряє з'єднання з PostgreSQL.
    2. Повертає статус 200, якщо все гаразд.
    """
    try:
        # Спроба виконати найпростіший SQL запит
        await db.execute(text("SELECT 1"))
        return {
            "status": "online",
            "database": "connected",
            "message": "System is healthy"
        }
    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )