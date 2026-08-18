from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.session import async_session
from app.models.application import Application  # Припустима модель заявки
from sqlalchemy import select

router = Router()

@router.callback_query(F.data == "owner_applications")
async def show_applications(callback: types.CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(Application).where(Application.status == "pending"))
        apps = result.scalars().all()

    if not apps:
        await callback.message.edit_text("📥 Наразі нових заявок немає.")
        return

    builder = InlineKeyboardBuilder()
    for app in apps:
        builder.button(text=f"👤 {app.full_name} ({app.role})", callback_data=f"app_view_{app.id}")
    builder.adjust(1)
    
    await callback.message.edit_text("📥 **Нові заявки на приєднання:**", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("app_view_"))
async def view_application(callback: types.CallbackQuery):
    app_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        app = await session.get(Application, app_id)
        
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Прийняти", callback_data=f"app_approve_{app_id}")
    builder.button(text="❌ Відхилити", callback_data=f"app_reject_{app_id}")
    
    await callback.message.edit_text(
        f"📋 **Заявка #{app_id}**\n\n"
        f"Ім'я: {app.full_name}\n"
        f"Навичка: {app.skills}\n"
        f"Контакт: @{app.username}",
        reply_markup=builder.as_markup()
    )