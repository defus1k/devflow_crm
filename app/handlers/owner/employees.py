from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.db.session import async_session
from app.models.user import User
from app.keyboards.owner.employees import get_owner_employees_kb, get_role_selection_kb
from sqlalchemy import select

router = Router()

# 1. Список всіх працівників
@router.callback_query(F.data == "owner_employees_list")
async def show_employees(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
    
    await callback.message.edit_text(
        "👥 Список користувачів (оберіть для зміни ролі):",
        reply_markup=get_owner_employees_kb(users)
    )

# 2. Вибір ролі для конкретного користувача
@router.callback_query(F.data.startswith("edit_role_"))
async def select_role(callback: CallbackQuery):
    user_id = callback.data.split("_")[2]
    await callback.message.edit_text(
        "Оберіть нову роль для користувача:",
        reply_markup=get_role_selection_kb(user_id)
    )

# 3. Збереження нової ролі в БД
@router.callback_query(F.data.startswith("set_role_"))
async def save_role(callback: CallbackQuery):
    # Формат: set_role_ROLE_USERID
    _, _, new_role, user_id = callback.data.split("_")
    
    async with async_session() as session:
        user = await session.get(User, int(user_id))
        if user:
            user.role = new_role
            await session.commit()
            await callback.answer(f"Роль змінено на {new_role}!", show_alert=True)
        else:
            await callback.answer("Користувача не знайдено.")

    await callback.message.edit_text("Роль успішно оновлено!")