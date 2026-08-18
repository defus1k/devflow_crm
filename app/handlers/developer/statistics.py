from aiogram import F, Router, types

from app.db.session import async_session
from app.services.developer_service import DeveloperService

router = Router()


@router.callback_query(F.data == "dev_statistics")
async def show_dev_stats(callback: types.CallbackQuery):
    async with async_session() as session:
        service = DeveloperService(session)
        stats = await service.get_project_stats(callback.from_user.id)

    stats_text = (
        "📊 Моя статистика\n\n"
        f"✅ Завершені: {stats['completed']}\n"
        f"⏳ В роботі: {stats['in_progress']}\n"
        f"🧪 На перевірці: {stats['under_review']}\n"
        f"💰 Загальний заробіток: {stats['total_income']:.2f}"
    )

    await callback.message.answer(stats_text)
    await callback.answer()