from aiogram.types import ReplyKeyboardRemove
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.db.session import async_session
from app.models.application import Application
from app.core.config import settings as config

from app.keyboards.client.menu import get_main_menu_kb
from app.keyboards.common.worker_application import (
    get_position_kb,
    get_continue_kb,
    get_application_confirm_kb,
    get_owner_application_kb
)

router = Router()


# =========================
# FSM
# =========================

class WorkerForm(StatesGroup):
    position = State()
    name = State()
    age = State()
    experience = State()
    skills = State()
    portfolio = State()
    motivation = State()
    online = State()


# =========================
# Початок
# =========================

@router.message(Command("worker_application"))
@router.message(F.text == "💼 Стати працівником")
async def start_application(message: types.Message, state: FSMContext):

    await state.clear()

   

    await message.answer(
        "💼 <b>Подання заявки</b>\n\n"
        "Оберіть посаду, на яку бажаєте подати заявку.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
        
    )

    await message.answer(
        "👇 Оберіть посаду:",
        reply_markup=get_position_kb()
    )


# =========================
# Менеджер
# =========================

@router.callback_query(F.data == "position_manager")
async def manager_description(callback: types.CallbackQuery, state: FSMContext):

    await state.update_data(position="Менеджер")
    await state.set_state(WorkerForm.position)

    text = (
        "👨‍💼 <b>Менеджер</b>\n\n"
        """Хто такий менеджер в Nexora BotForge:
Це обличчя команди, яке відповідає за успіх проєкту. Ви не просто "передаєте слова", ви структуруєте хаос у технічне завдання.

Ваші обов'язки:
• <b>Виявлення потреб:</b> Ви повинні розуміти, яку бізнес-задачу вирішує клієнт.
• <b>Брифінг:</b> Збір технічних вимог за шаблоном, щоб розробник одразу бачив повну картину.
• <b>Контроль:</b> Ви — гарант того, що розробник отримав усі файли, API-ключі та опис логіки до початку роботи.
• <b>TikTok:</b> Кожні <b>48 годин</b> ви зобов'язані публікувати щонайменше одне відео з рекламою <b>Nexora BotForge</b>. Відео може бути створене за допомогою AI або будь-яким іншим способом, але повинно бути якісним, цікавим та спрямованим на залучення нових клієнтів.

Якщо вас усе влаштовує — натисніть «Продовжити»."""
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_continue_kb()
    )


# =========================
# Python Developer
# =========================

@router.callback_query(F.data == "position_python")
async def developer_description(callback: types.CallbackQuery, state: FSMContext):

    await state.update_data(position="Python Developer")
    await state.set_state(WorkerForm.position)

    text = (
        "👨‍💻 <b>Python Developer (Bot Specialist)</b>\n\n"
        """Хто такий IT-спеціаліст в Nexora BotForge:
Ми спеціалізуємося на створенні інтелектуальних систем автоматизації, тому ви — ключовий архітектор наших бот-рішень.

Ваші обов'язки:
• <b>Розробка:</b> Створення професійних Telegram та Discord ботів з нуля — від простої логіки до складних CRM-систем.
• <b>Аналіз ТЗ:</b> Робота з чітко структурованими заявками, які готує наш менеджер.
• <b>Якість:</b> Написання стабільного, чистого коду та своєчасне оновлення функціоналу під API Telegram/Discord.
• <b>Стек:</b> Робота з базами даних (SQL) та хмарними сервісами для забезпечення безперебійної роботи ботів.

Якщо ви майстер створення ботів і готові до складних проєктів — натисніть «Продовжити»."""
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_continue_kb()
    )


# =========================
# Назад
# =========================

@router.callback_query(F.data == "application_back")
async def back_to_positions(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "💼 Оберіть посаду:",
        reply_markup=get_position_kb()
    )


# =========================
# Почати анкету
# =========================

@router.callback_query(F.data == "application_continue")
async def start_form(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "👤 Як вас звати?"
    )

    await state.set_state(WorkerForm.name)


# =========================
# Скасування
# =========================

@router.callback_query(F.data == "cancel_application")
async def cancel_application(callback: types.CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.edit_text(
        "❌ Подання заявки скасовано."
    )

    await callback.message.answer(
        "Головне меню:",
        reply_markup=get_main_menu_kb()
    )


# =========================
# Ім'я
# =========================

@router.message(WorkerForm.name)
async def form_name(message: types.Message, state: FSMContext):

    await state.update_data(
        applicant_name=message.text
    )

    await message.answer(
        "🎂 Скільки вам років?"
    )

    await state.set_state(
        WorkerForm.age
    )


# =========================
# Вік
# =========================

# =========================
# Вік
# =========================

@router.message(WorkerForm.age)
async def form_age(message: types.Message, state: FSMContext):
    # Зберігаємо вік, який ввів користувач
    await state.update_data(age=message.text)
    
    # Отримуємо дані, щоб зрозуміти, на яку посаду подається кандидат
    data = await state.get_data()
    position = data.get("position")

    # Формуємо текст питання залежно від посади
    if position == "Python Developer":
        question = "🐍 Скільки часу ви займаєтесь програмуванням?"
    else:
        question = "💼 Який у вас досвід роботи в менеджменті або продажах?"

    # Відправляємо відповідне питання
    await message.answer(question)
    
    # Переходимо до кроку досвіду
    await state.set_state(WorkerForm.experience)


# =========================
# Досвід
# =========================

@router.message(WorkerForm.experience)
async def form_experience(message: types.Message, state: FSMContext):

    await state.update_data(
        experience=message.text
    )

    data = await state.get_data()

    if data.get("position") == "Python Developer":
        text = (
            "💻 Опишіть свої технічні навички.\n\n"
            "Наприклад:\n\n"
            "• Python\n"
            "• Aiogram\n"
            "• pyTelegramBotAPI\n"
            "• Pyrogram\n"
            "• Telethon\n"
            "• discord.py\n"
            "• disnake\n"
            "• SQLAlchemy\n"
            "• AsyncPG\n"
            "• PostgreSQL\n"
            "• Docker\n"
            "• Git\n\n"
            "Якщо працювали з іншими технологіями або бібліотеками — також можете їх вказати."
    )
    else:
        text = (
            "💼 Опишіть свої навички.\n\n"
            "Наприклад:\n\n"
            "• Спілкування з клієнтами\n"
            "• Продажі\n"
            "• Ведення проєктів\n"
            "• Робота із запереченнями\n"
            "• CRM-системи\n"
            "• Постановка задач\n"
            "• Робота в команді\n\n"
            "Якщо маєте інші навички — також можете їх вказати."
    )

    await message.answer(text)
    await state.set_state(WorkerForm.skills)

    await state.set_state(
    WorkerForm.skills
    )
    # =========================
# Навички
# =========================

@router.message(WorkerForm.skills)
async def form_skills(message: types.Message, state: FSMContext):

    await state.update_data(
        skills=message.text
    )

    data = await state.get_data()

    if data.get("position") == "Python Developer":
        text = (
        "🤖 Розкажіть про свої проєкти.\n\n"
        "Опишіть Telegram або Discord ботів, яких ви вже створювали.\n\n"
        "Також можете надіслати:\n"
        "• GitHub\n"
        "• GitLab\n"
        "• Google Drive\n"
        "• Інше портфоліо"
    )
    else:
        text = (
        "📂 Розкажіть про свій досвід роботи.\n\n"
        "Якщо вже працювали менеджером — коротко опишіть, "
        "які проєкти вели або який маєте досвід.\n\n"
        "Якщо маєте портфоліо, резюме або приклади робіт — "
        "можете надіслати посилання."
    )

    await message.answer(text)

    await state.set_state(
    WorkerForm.portfolio
)

    await state.set_state(
        WorkerForm.portfolio
    )


# =========================
# Проєкти
# =========================

@router.message(WorkerForm.portfolio)
async def form_portfolio(message: types.Message, state: FSMContext):

    await state.update_data(
        portfolio=message.text
    )

    await message.answer(
        "💬 Чому саме ви хочете приєднатися до нашої команди?"
    )

    await state.set_state(
        WorkerForm.motivation
    )


# =========================
# Мотивація
# =========================

@router.message(WorkerForm.motivation)
async def form_motivation(message: types.Message, state: FSMContext):

    await state.update_data(
        motivation=message.text
    )

    await message.answer(
        "⏰ Скільки годин на день ви готові приділяти роботі?"
    )

    await state.set_state(
        WorkerForm.online
    )


# =========================
# Онлайн
# =========================

@router.message(WorkerForm.online)
async def form_online(message: types.Message, state: FSMContext):

    await state.update_data(
        online=message.text
    )

    data = await state.get_data()

    text = (
        "📄 <b>Перевірте заявку</b>\n\n"

        f"💼 <b>Посада:</b> {data['position']}\n"
        f"👤 <b>Ім'я:</b> {data['applicant_name']}\n"
        f"🎂 <b>Вік:</b> {data['age']}\n"
        f"📅 <b>Досвід:</b> {data['experience']}\n\n"

        f"📚 <b>Навички:</b>\n{data['skills']}\n\n"

        f"🤖 <b>Проєкти / GitHub:</b>\n{data['portfolio']}\n\n"

        f"💬 <b>Чому саме ви:</b>\n{data['motivation']}\n\n"

        f"⏰ <b>Онлайн:</b> {data['online']}"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_application_confirm_kb()
    )


# =========================
# Подати заявку
# =========================

@router.callback_query(F.data == "submit_application")
async def submit_application(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Если данные пустые — не даем боту упасть
    if not data:
        await callback.answer("Дані не знайдено, будь ласка, заповніть анкету заново.")
        return

    async with async_session() as session:
        application = Application(
            user_id=callback.from_user.id,
            position=data.get("position", "Не вказано"),
            topic=data.get("position", "Заявка"),
            applicant_name=data.get("applicant_name", "Не вказано"),
            age=data.get("age", "0"),
            experience=data.get("experience", "0"),
            skills=data.get("skills", "0"),
            portfolio=data.get("portfolio", "0"),
            motivation=data.get("motivation", "0"),
            online=data.get("online", "0"),
            status="pending",
            message="-",
        )
        session.add(application)
        await session.commit()
        await session.refresh(application)
        
    await callback.message.answer("Заявку успішно відправлено!")
    await state.clear() # Очищаем состояние только после успеха
    owner_text = (
        f"📨 <b>Нова заявка №{application.id}</b>\n\n"

        f"💼 <b>Посада:</b> {application.position}\n"
        f"👤 <b>Ім'я:</b> {application.applicant_name}\n"
        f"🎂 <b>Вік:</b> {application.age}\n"
        f"📅 <b>Досвід:</b> {application.experience}\n\n"

        f"📚 <b>Навички:</b>\n{application.skills}\n\n"

        f"🤖 <b>Проєкти:</b>\n{application.portfolio}\n\n"

        f"💬 <b>Мотивація:</b>\n{application.motivation}\n\n"

        f"⏰ <b>Онлайн:</b> {application.online}\n\n"

        f"👤 @{callback.from_user.username or 'без username'}\n"

        f"<a href='tg://user?id={callback.from_user.id}'>Написати кандидату</a>"
    )

    if data["position"] == "Менеджер":
        forum_id = config.MANAGER_FORUM_ID
    else:
        forum_id = config.DEVELOPER_FORUM_ID

    await callback.bot.send_message(
        chat_id=forum_id,
        text=owner_text,
        parse_mode="HTML",
        reply_markup=get_owner_application_kb(application.id)
    )

    await callback.message.edit_text(
        "✅ Вашу заявку успішно відправлено."
    )

    await callback.message.answer(
        "Головне меню:",
        reply_markup=get_main_menu_kb()
    )

    await state.clear()


# =========================
# Заповнити заново
# =========================

@router.callback_query(F.data == "restart_application")
async def restart_application(callback: types.CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.edit_text(
        "💼 Оберіть посаду:",
        reply_markup=get_position_kb()
    )


# =========================
# Прийняти
# =========================

@router.callback_query(F.data.startswith("accept_application:"))
async def accept_application(callback: types.CallbackQuery):

    await callback.answer("Заявку прийнято!")

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        "✅ Кандидата прийнято."
    )


# =========================
# Відхилити
# =========================

@router.callback_query(F.data.startswith("reject_application:"))
async def reject_application(callback: types.CallbackQuery):

    await callback.answer("Заявку відхилено!")

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        "❌ Кандидата відхилено."
    )