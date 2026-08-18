import asyncio

from app.db.base import Base
from app.db.session import engine

import app.models


async def create():
    print("=" * 50)
    print("DATABASE:", engine.url)
    print("=" * 50)

    print("Models in metadata:")

    for table in Base.metadata.tables:
        print(table)

    print("COUNT =", len(Base.metadata.tables))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("DONE")


asyncio.run(create())