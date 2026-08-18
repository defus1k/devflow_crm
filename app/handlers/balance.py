from decimal import Decimal

from aiogram import Router, types
from aiogram.filters import Command

from app.db.session import async_session
from app.models.user import User
from app.core.config import settings


router = Router()


# ==========================
# Проверка баланса
# ==========================

@router.message(Command("balance"))
async def check_balance(message: types.Message):

    async with async_session() as session:
        user = await session.get(
            User,
            message.from_user.id
        )

    if not user:
        await message.answer(
            "❌ Пользователь не найден."
        )
        return


    balance = user.balance or Decimal("0.00")


    await message.answer(
        f"""
💰 Ваш баланс

👤 {user.full_name}

💵 {balance:.2f} грн
"""
    )



# ==========================
# Добавить баланс (OWNER)
# ==========================

@router.message(Command("add_balance"))
async def add_balance(message: types.Message):

    if message.from_user.id != settings.OWNER_ID:
        await message.answer(
            "❌ Нет доступа."
        )
        return


    args = message.text.split()


    if len(args) != 3:
        await message.answer(
            "Использование:\n"
            "/add_balance ID СУММА"
        )
        return


    try:
        user_id = int(args[1])
        amount = Decimal(args[2])

    except Exception:
        await message.answer(
            "❌ Неверная сумма."
        )
        return



    async with async_session() as session:

        user = await session.get(
            User,
            user_id
        )


        if not user:
            await message.answer(
                "❌ Пользователь не найден."
            )
            return


        user.balance += amount

        await session.commit()



    await message.answer(
        f"""
✅ Баланс пополнен

👤 ID: {user_id}

💰 +{amount:.2f} грн
"""
    )



# ==========================
# Снять баланс (OWNER)
# ==========================

@router.message(Command("remove_balance"))
async def remove_balance(message: types.Message):

    if message.from_user.id != settings.OWNER_ID:
        await message.answer(
            "❌ Нет доступа."
        )
        return


    args = message.text.split()


    if len(args) != 3:
        await message.answer(
            "Использование:\n"
            "/remove_balance ID СУММА"
        )
        return


    try:
        user_id = int(args[1])
        amount = Decimal(args[2])

    except Exception:
        await message.answer(
            "❌ Неверная сумма."
        )
        return



    async with async_session() as session:

        user = await session.get(
            User,
            user_id
        )


        if not user:
            await message.answer(
                "❌ Пользователь не найден."
            )
            return


        current = user.balance or Decimal("0.00")


        if current < amount:
            await message.answer(
                "❌ Недостаточно средств."
            )
            return


        user.balance -= amount

        await session.commit()



    await message.answer(
        f"""
✅ Баланс уменьшен

👤 ID: {user_id}

💸 -{amount:.2f} грн
"""
    )