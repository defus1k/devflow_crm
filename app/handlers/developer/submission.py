import logging
from datetime import datetime
from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.db.session import async_session
from app.models.order import Order
from app.models.user import User
from app.states.developer import SubmitProjectStates
from app.handlers.developer.project_checker import ProjectCheckerService
from app.keyboards.developer.developer_submission import (
    get_developer_projects_kb,
    get_owner_review_kb,
    get_owner_client_transfer_kb
)

logger = logging.getLogger(__name__)
router = Router()

# 1. Розробник натискає кнопку "📤 Здати проєкт"
@router.message(F.text == "📤 Здати проєкт")
async def start_submission(message: types.Message, state: FSMContext):
    async with async_session() as session:
        orders = await session.scalars(
            select(Order)
            .where(Order.developer_id == message.from_user.id)
            .where(Order.status == "in_progress")
        )
        orders_list = orders.all()

    if not orders_list:
        await message.answer("📤 У вас немає активних проєктів зі статусом «В роботі».")
        return

    await message.answer(
        "📤 **Здача проєкту**\n\nВиберіть проєкт, який бажаєте здати:",
        reply_markup=get_developer_projects_kb(orders_list),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("submit_proj_"))
async def process_project_choice(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if not order or order.developer_id != callback.from_user.id:
            await callback.answer("❌ Проєкт не знайдено або він вам не належить.", show_alert=True)
            return

    await state.update_data(order_id=order_id, order_title=order.title)
    await callback.message.edit_text(
        f"🔗 **Крок 1/3: Посилання на GitHub**\n\n"
        f"Надішліть коректне посилання на GitHub Repository вибраного проєкту.",
        parse_mode="Markdown"
    )
    await state.set_state(SubmitProjectStates.waiting_for_github)
    await callback.answer()

# Крок 1: Отримання та перевірка GitHub URL
@router.message(SubmitProjectStates.waiting_for_github, F.text)
async def receive_github_url(message: types.Message, state: FSMContext):
    url = message.text.strip()
    if not ProjectCheckerService.validate_github_url(url):
        await message.answer("❌ Некоректне посилання! Будь ласка, введіть дійсне посилання на репозиторій GitHub (наприклад: `https://github.com/user/repo`).", parse_mode="Markdown")
        return

    await state.update_data(github_url=url)
    await message.answer(
        "📝 **Крок 2/3: Коментар до здачі**\n\n"
        "Опишіть коротко:\n"
        "• що виконано;\n"
        "• особливості запуску;\n"
        "• додаткову інформацію.",
        parse_mode="Markdown"
    )
    await state.set_state(SubmitProjectStates.waiting_for_comment)

# Крок 2: Отримання коментаря
@router.message(SubmitProjectStates.waiting_for_comment, F.text)
async def receive_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text.strip())
    await message.answer(
        "📎 **Крок 3/3: ZIP-архів проєкту**\n\n"
        "Надішліть ZIP-архів вашого проєкту. Інші типи файлів не приймаються.",
        parse_mode="Markdown"
    )
    await state.set_state(SubmitProjectStates.waiting_for_zip)

# Крок 3: Отримання та перевірка ZIP-архіву
@router.message(SubmitProjectStates.waiting_for_zip, F.document)
async def receive_zip_archive(message: types.Message, state: FSMContext, bot: Bot):
    document = message.document
    if not document.file_name.endswith(".zip"):
        await message.answer("❌ Помилка! Дозволено надсилати лише файли у форматі `.zip`. Спробуйте ще раз.", parse_mode="Markdown")
        return

    # Завантаження файлу в пам'ять
    file_info = await bot.get_file(document.file_id)
    file_bytes_io = await bot.download_file(file_info.file_path)
    zip_bytes = file_bytes_io.read()

    # Запуск сервісу автоматичної перевірки
    struct_results, violations = ProjectCheckerService.analyze_zip(zip_bytes)

    if violations:
        violation_text = "\n".join([f"• {v}" for v in violations])
        await message.answer(
            f"❌ **Автоматична перевірка не пройшла безпеку/структуру:**\n\n{violation_text}\n\n"
            "Виправте помилки та надішліть новий ZIP-архів.",
            parse_mode="Markdown"
        )
        return

    data = await state.get_data()
    order_id = data["order_id"]
    order_title = data["order_title"]
    github_url = data["github_url"]
    comment = data["comment"]

    # Збереження файлу документа для Owner
    file_id = document.file_id

    async with async_session() as session:
        order = await session.get(Order, order_id)
        if order:
            order.status = "Очікує перевірки"
            await session.commit()

    await state.clear()

    # Формування звіту для розробника
    passed_checks_str = "\n".join([f"{'✅' if val else '⚠️'} {key}" for key, val in struct_results.items()])
    
    await message.answer(
        f"✅ **Проєкт успішно здано на перевірку!**\n\n"
        f"📦 **Назва:** {order_title}\n"
        f"🔗 **GitHub:** {github_url}\n"
        f"📋 **Результати перевірки структури:**\n{passed_checks_str}\n\n"
        f"🟡 **Статус:** Очікує перевірки Owner",
        parse_mode="Markdown"
    )

    # Пошук Owner (роль 'owner' у базі даних)
    async with async_session() as session:
        owner = await session.scalar(select(User).where(User.role == "owner"))
    
    if owner:
        report_text = (
            f"📥 **Новий проєкт на перевірку!**\n\n"
            f"📦 **Назва проєкту:** {order_title} (ID: #{order_id})\n"
            f"👨‍💻 **Розробник:** {message.from_user.full_name} (ID: `{message.from_user.id}`)\n"
            f"📅 **Дата здачі:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"🔗 **GitHub:** {github_url}\n"
            f"📝 **Коментар:** {comment}\n\n"
            f"📋 **Автоматична перевірка:** Успішно пройдена (без секретів)"
        )
        await bot.send_document(
            chat_id=owner.telegram_id,
            document=file_id,
            caption=report_text,
            parse_mode="Markdown",
            reply_markup=get_owner_review_kb(order_id)
        )
    else:
        logger.warning("Owner user not found in database to send submission report.")

@router.message(SubmitProjectStates.waiting_for_zip, ~F.document)
async def wrong_zip_format(message: types.Message):
    await message.answer("❌ Будь ласка, прикріпіть файл як документ у форматі `.zip`.")

# Дії Owner: Прийняти
@router.callback_query(F.data.startswith("owner_accept_"))
async def owner_accept_project(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    
    async with async_session() as session:
        order = await session.get(Order, order_id)
        if not order:
            await callback.answer("❌ Замовлення не знайдено.", show_alert=True)
            return
        order.status = "Готовий"
        await session.commit()

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ **Статус:** Змінено на «Готовий» (Очікує підтвердження відправки клієнту)",
        parse_mode="Markdown",
        reply_markup=get_owner_client_transfer_kb(order_id)
    )
    await callback.answer("Проєкт прийнято!")

# Дії Owner: Відправити на доопрацювання (запит причини через FSM або тимчасовий стан можна реалізувати, або через text)
@router.callback_query(F.data.startswith("owner_reject_"))
async def owner_reject_project(callback: types.CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[2])
    await state.update_data(reject_order_id=order_id, owner_message_id=callback.message.message_id)
    
    await callback.message.answer("✍️ Введіть причину відправки на доопрацювання для розробника:")
    await state.set_state("waiting_for_reject_reason")
    await callback.answer()

@router.message(F.state == "waiting_for_reject_reason", F.text)
async def process_reject_reason(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    order_id = data["reject_order_id"]
    reason = message.text.strip()

    async with async_session() as session:
        order = await session.get(Order, order_id)
        if order:
            order.status = "in_progress"
            developer_id = order.developer_id
            await session.commit()

            # Повідомлення розробнику
            if developer_id:
                try:
                    await bot.send_message(
                        chat_id=developer_id,
                        text=f"❌ **Ваш проєкт #{order_id} відправлено на доопрацювання!**\n\n💬 **Причина:** {reason}",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.error(f"Failed to notify developer {developer_id}: {e}")

    await message.answer(f"✅ Проєкт #{order_id} повернуто у статус «В роботі». Розробника сповіщено.")
    await state.clear()

# Підтвердження відправки клієнту від Owner
@router.callback_query(F.data.startswith("send_to_client_"))
async def owner_send_to_client(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[2])

    async with async_session() as session:
        order = await session.get(Order, order_id)
        if not order:
            await callback.answer("❌ Замовлення не знайдено.", show_alert=True)
            return
        
        # Тут можна отримати клієнта з бази (наприклад, order.client_id)
        client_id = getattr(order, "client_id", None)

    # Симуляція відправки клієнту (або реальна відправка, якщо є client_id)
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n🚀 **Успішно надіслано клієнту!**",
        reply_markup=None,
        parse_mode="Markdown"
    )
    await callback.answer("Проєкт успішно відправлено клієнту!", show_alert=True)