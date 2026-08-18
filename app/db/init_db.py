from app.db.base import Base
from app.db.session import engine

# импортируем ВСЕ модели
from app.models.user import User
from app.models.order import Order
from app.models.payment import Payment
from app.models.review import Review
from app.models.application import Application
from app.models.portfolio import Portfolio
from app.models.withdrawal import Withdrawal
from app.models.ticket import Ticket
from app.models.balance import Balance
from app.models.kpi import KPI
from app.models.log import Log
from app.models.statistics import Statistics
from app.models.notification import Notification
from app.models.warning import Warning

import asyncio


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())