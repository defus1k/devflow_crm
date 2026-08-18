from aiogram import F, Router, types

from app.db.session import async_session
from app.services.developer_service import DeveloperService

router = Router()


@router.callback_query(F.data == "dev_salary")
async def show_dev_salary(callback: types.CallbackQuery):
    async with async_session() as session:
        service = DeveloperService(session)
        stats = await service.get_project_stats(callback.from_user.id)

    await callback.message.answer(
        f"💰 Ваш звіт\n\n"
        f"✅ Завершено: {stats['completed']}\n"
        f"⏳ На перевірці: {stats['under_review']}\n"
        f"💵 Заробіток: {stats['total_income']:.2f}"
    )
    await callback.answer()