import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/devflow_crm"

async def main():
    engine = create_async_engine(DATABASE_URL)

    try:
        async with engine.begin():
            print("✅ Подключение успешно")
    except Exception as e:
        print(type(e).__name__)
        print(e)

    await engine.dispose()

asyncio.run(main())