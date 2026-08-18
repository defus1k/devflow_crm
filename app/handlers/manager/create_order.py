import os
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.core.config import settings
from sqlalchemy import select
from app.models.order import Order
from app.db.session import async_session

router = Router()

COUNTER_FILE = "order_counter.txt"

def get_next_order_number():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            try:
                current = int(f.read().strip())
            except ValueError:
                current = 0
    else:
        current = 0
    
    next_number = current + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(next_number))
    return next_number


# =========================
# FSM СТАНИ ЗАМОВЛЕННЯ
# =========================

class OrderCreation(StatesGroup):
    selected_db_order_id = State() # Спершу вибираємо/вводимо ID замовлення з БД
    platform = State()
    title = State()
    description = State()
    features = State()
    examples = State()
    integrations = State()
    admin_panel = State()
    database_need = State()
    has_spec = State()
    additional_materials = State()
    deadline = State()
    budget = State()
    wishes = State()
    preview = State()


# =========================
# КЛАВІАТУРИ
# =========================

def get_platform_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🤖 Telegram", callback_data="platform_telegram")
    builder.button(text="🎮 Discord", callback_data="platform_discord")
    builder.adjust(2)
    return builder.as_markup()

def get_yes_no_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Так", callback_data="ans_yes")
    builder.button(text="❌ Ні", callback_data="ans_no")
    builder.adjust(2)
    return builder.as_markup()

def get_confirm_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Підтвердити і передати в ІТ", callback_data="confirm_order_yes")
    builder.button(text="❌ Скасувати", callback_data="confirm_order_no")
    builder.adjust(1)
    return builder.as_markup()


# =========================
# КРОК 1: ВИБІР ЗАМОВЛЕННЯ МЕНЕДЖЕРОМ
# =========================

@router.message(F.text == "📥 Передати замовлення в ІТ")
async def start_order_creation(message: Message, state: FSMContext):
    await state.clear()
    
    # Шукаємо замовлення цього менеджера/клієнта в базі, які ще не відправлені або нові
    async with async_session() as session:
        result = await session.execute(
            select(Order).filter(Order.user_id == message.from_user.id).order_by(Order.created_at.desc()).limit(10)
        )
        user_orders = result.scalars().all()

    builder = InlineKeyboardBuilder()
    
    # Якщо є існуючі замовлення в базі, даємо вибір
    if user_orders:
        for ord_obj in user_orders:
            builder.button(
                text=f"📦 Замовлення #{ord_obj.id} ({ord_obj.status})", 
                callback_data=f"pick_order:{ord_obj.id}"
            )
    
    # Кнопка створення нового
    builder.button(text="➕ Створити нове унікальне замовлення", callback_data="pick_order:new")
    builder.adjust(1)

    await message.answer(
        "<b>Виберіть замовлення з бази, яке хочете відправити в ІТ, або створіть нове:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    # Встановлюємо початковий стан вибору
    await state.set_state(OrderCreation.selected_db_order_id)


@router.callback_query(OrderCreation.selected_db_order_id, F.data.startswith("pick_order:"))
async def process_picked_order(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]
    
    if action == "new":
        order_id = get_next_order_number()
    else:
        order_id = int(action)

    await state.update_data(order_id=order_id)
    
    await callback.message.edit_text(
        f"✅ Обрано замовлення ID: <b>#{order_id}</b>\n\n"
        "<b>1. Для якої платформи потрібен бот?</b>",
        reply_markup=get_platform_kb(),
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.platform)
    await callback.answer()


# =========================
# ПЛАТФОРМА
# =========================

@router.callback_query(OrderCreation.platform, F.data.startswith("platform_"))
async def process_platform(callback: CallbackQuery, state: FSMContext):
    platform = "Telegram" if "telegram" in callback.data else "Discord"
    await state.update_data(platform=platform)
    await callback.message.edit_text(
        f"Платформа: <b>{platform}</b>\n\n"
        f"<b>2. Введіть назву проєкту:</b>",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.title)
    await callback.answer()


# =========================
# НАЗВА
# =========================

@router.message(OrderCreation.title)
async def process_title(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть текст.")
    await state.update_data(title=text)
    await message.answer(
        "<b>3. Що повинен робити бот?</b>\n\n"
        "(Напишіть детальний опис функціоналу):",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.description)


# =========================
# ОПИС
# =========================

@router.message(OrderCreation.description)
async def process_description(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть текстовий опис.")
    await state.update_data(description=text)
    await message.answer(
        "<b>4. Які команди або функції повинні бути?</b>\n\n"
        "(Наприклад: модерація, заявки, магазин, CRM тощо):",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.features)


# =========================
# ФУНКЦІЇ
# =========================

@router.message(OrderCreation.features)
async def process_features(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть текст з описом функцій.")
    await state.update_data(features=text)
    await message.answer(
        "<b>5. Чи є приклади ботів?</b>\n\n"
        "(Посилання, або опис):",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.examples)


# =========================
# ПРИКЛАДИ
# =========================

@router.message(OrderCreation.examples)
async def process_examples(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть текстове повідомлення або посилання.")
    await state.update_data(examples=text)
    await message.answer(
        "<b>6. Чи потрібне підключення до сторонніх сервісів / баз даних?</b>\n\n"
        "(PostgreSQL, MySQL, API, OpenAI, Google Sheets тощо):",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.integrations)


# =========================
# ІНТЕГРАЦІЇ
# =========================

@router.message(OrderCreation.integrations)
async def process_integrations(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть текстову відповідь.")
    await state.update_data(integrations=text)
    await message.answer(
        "<b>7. Чи потрібна адмін-панель?</b>",
        reply_markup=get_yes_no_kb(),
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.admin_panel)


# =========================
# АДМІНКА
# =========================

@router.callback_query(OrderCreation.admin_panel, F.data.startswith("ans_"))
async def process_admin_panel(callback: CallbackQuery, state: FSMContext):
    ans = "Так" if "yes" in callback.data else "Ні"
    await state.update_data(admin_panel=ans)
    await callback.message.edit_text(
        f"Адмін-панель: <b>{ans}</b>\n\n"
        "<b>8. Чи потрібне зберігання даних (БД)?</b>",
        reply_markup=get_yes_no_kb(),
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.database_need)
    await callback.answer()


# =========================
# БАЗА ДАНИХ
# =========================

@router.callback_query(OrderCreation.database_need, F.data.startswith("ans_"))
async def process_db_need(callback: CallbackQuery, state: FSMContext):
    ans = "Так" if "yes" in callback.data else "Ні"
    await state.update_data(database_need=ans)
    await callback.message.edit_text(
        f"База даних: <b>{ans}</b>\n\n"
        "<b>9. Чи є готове технічне завдання (ТЗ)?</b>",
        reply_markup=get_yes_no_kb(),
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.has_spec)
    await callback.answer()


# =========================
# ТЗ
# =========================

@router.callback_query(OrderCreation.has_spec, F.data.startswith("ans_"))
async def process_has_spec(callback: CallbackQuery, state: FSMContext):
    ans = "Так" if "yes" in callback.data else "Ні"
    await state.update_data(has_spec=ans)
    
    done_kb = InlineKeyboardBuilder()
    done_kb.button(text="➡️ Готово / Далі", callback_data="materials_done")
    
    await callback.message.edit_text(
        f"Готове ТЗ: <b>{ans}</b>\n\n"
        "<b>10. Додаткові матеріали</b>\n\n"
        "Надішліть файли, фото, документи або напишіть текстом. Коли закінчите, натисніть кнопку нижче:",
        reply_markup=done_kb.as_markup(),
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.additional_materials)
    await callback.answer()


# =========================
# МАТЕРІАЛИ
# =========================

@router.message(OrderCreation.additional_materials)
async def process_materials_msg(message: Message, state: FSMContext):
    data = await state.get_data()
    materials = data.get("additional_materials", [])

    if message.text:
        materials.append({"type": "text", "value": message.text})
    if message.photo:
        materials.append({"type": "photo", "file_id": message.photo[-1].file_id})
    if message.document:
        materials.append({"type": "document", "file_id": message.document.file_id})
    if message.video:
        materials.append({"type": "video", "file_id": message.video.file_id})
    if message.animation:
        materials.append({"type": "animation", "file_id": message.animation.file_id})
    if message.voice:
        materials.append({"type": "voice", "file_id": message.voice.file_id})
    if message.audio:
        materials.append({"type": "audio", "file_id": message.audio.file_id})

    await state.update_data(additional_materials=materials)
    await message.react([{"type": "emoji", "emoji": "👍"}])


@router.callback_query(OrderCreation.additional_materials, F.data == "materials_done")
async def process_materials_done(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    materials = data.get("additional_materials", [])

    if not materials:
        materials.append({"type": "text", "value": "Немає"})
        await state.update_data(additional_materials=materials)

    await callback.message.answer(
        "<b>11. Вкажіть термін виконання:</b>\n\n"
        "Наприклад: 20 днів",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.deadline)
    await callback.answer()


# =========================
# ДЕДЛАЙН
# =========================

@router.message(OrderCreation.deadline)
async def process_deadline(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть термін виконання текстом.")
    await state.update_data(deadline=text)
    await message.answer(
        "<b>12. Вкажіть бюджет проєкту:</b>\n\n"
        "Наприклад: 10000 грн",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.budget)


# =========================
# БЮДЖЕТ
# =========================

@router.message(OrderCreation.budget)
async def process_budget(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть бюджет текстом.")
    await state.update_data(budget=text)
    await message.answer(
        "<b>13. Додаткові побажання:</b>\n\n"
        "Якщо немає — напишіть «Немає»",
        parse_mode="HTML"
    )
    await state.set_state(OrderCreation.wishes)


# =========================
# ПРЕВ'Ю
# =========================

@router.message(OrderCreation.wishes)
async def process_wishes(message: Message, state: FSMContext):
    text = message.text or message.caption
    if not text:
        return await message.answer("Будь ласка, надішліть побажання текстом.")

    await state.update_data(wishes=text)
    data = await state.get_data()

    preview_text = (
        f"📦 <b>Перевірка замовлення #{data.get('order_id')}</b>\n\n"
        f"🤖 1. Платформа: {data.get('platform')}\n"
        f"📌 2. Назва: {data.get('title')}\n"
        f"📄 3. Опис: {data.get('description')}\n"
        f"⚙️ 4. Функції: {data.get('features')}\n"
        f"🔍 5. Приклади: {data.get('examples')}\n"
        f"🔗 6. Інтеграції: {data.get('integrations')}\n"
        f"🖥 7. Адмін-панель: {data.get('admin_panel')}\n"
        f"🗄 8. База даних: {data.get('database_need')}\n"
        f"📋 9. ТЗ: {data.get('has_spec')}\n"
        f"📎 10. Матеріалів додано: {len(data.get('additional_materials', []))}\n"
        f"⏳ 11. Термін виконання: {data.get('deadline')}\n"
        f"💰 12. Бюджет: {data.get('budget')}\n"
        f"📝 13. Побажання: {data.get('wishes')}"
    )

    await message.answer(preview_text, reply_markup=get_confirm_kb(), parse_mode="HTML")
    await state.set_state(OrderCreation.preview)


# =========================
# СКАСУВАННЯ
# =========================

@router.callback_query(OrderCreation.preview, F.data == "confirm_order_no")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Замовлення скасовано")
    await callback.answer()


# =========================
# СТВОРЕННЯ ВІТКИ ТА ЗПИС У БАЗУ ДАНИХ
# =========================

@router.callback_query(OrderCreation.preview, F.data == "confirm_order_yes")
async def confirm_and_send_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    forum_id = settings.DEVELOPER_ORDER_ID
    
    order_id = data.get("order_id")
    manager_id = callback.from_user.id

    # Зберігаємо або оновлюємо замовлення в базі даних (статус pending)
    async with async_session() as session:
        res = await session.execute(select(Order).filter(Order.id == order_id))
        order = res.scalar_one_or_none()
        
        if order:
            order.status = "pending"
            order.description = data.get('title')
        else:
            new_order = Order(
                id=order_id,
                user_id=manager_id,
                status="pending",
                description=data.get('title')
            )
            session.add(new_order)
        await session.commit()

    topic = await callback.bot.create_forum_topic(
        chat_id=int(forum_id),
        name=f"#{order_id} | {data.get('title')}"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Взяти замовлення", callback_data=f"set_status:{order_id}:in_work")

    order_text = (
        f"📦 <b>НОВЕ ЗАМОВЛЕННЯ #{order_id}</b>\n\n"
        f"🤖 <b>1. Платформа:</b> {data.get('platform')}\n"
        f"📌 <b>2. Назва проєкту:</b> {data.get('title')}\n\n"
        f"📄 <b>3. Опис проєкту:</b>\n{data.get('description')}\n\n"
        f"⚙️ <b>4. Команди / Функції:</b>\n{data.get('features')}\n\n"
        f"🔍 <b>5. Приклади ботів:</b>\n{data.get('examples')}\n\n"
        f"🔗 <b>6. Інтеграції:</b>\n{data.get('integrations')}\n\n"
        f"🖥 <b>7. Адмін-панель:</b> {data.get('admin_panel')}\n"
        f"🗄 <b>8. База даних:</b> {data.get('database_need')}\n"
        f"📋 <b>9. Готове технічне завдання:</b> {data.get('has_spec')}\n\n"
        f"⏳ <b>11. Термін виконання:</b> {data.get('deadline')}\n"
        f"💰 <b>12. Бюджет:</b> {data.get('budget')}\n\n"
        f"📝 <b>13. Додаткові побажання:</b>\n{data.get('wishes')}"
    )

    await callback.bot.send_message(
        chat_id=int(forum_id),
        message_thread_id=topic.message_thread_id,
        text=order_text,
        reply_markup=kb.as_markup(),
        parse_mode="HTML"
    )

    # Надсилання матеріалів
    materials = data.get('additional_materials', [])
    for mat in materials:
        if mat["type"] == "photo":
            await callback.bot.send_photo(int(forum_id), message_thread_id=topic.message_thread_id, photo=mat["file_id"])
        elif mat["type"] == "document":
            await callback.bot.send_document(int(forum_id), message_thread_id=topic.message_thread_id, document=mat["file_id"])
        elif mat["type"] == "video":
            await callback.bot.send_video(int(forum_id), message_thread_id=topic.message_thread_id, video=mat["file_id"])
        elif mat["type"] == "animation":
            await callback.bot.send_animation(int(forum_id), message_thread_id=topic.message_thread_id, animation=mat["file_id"])
        elif mat["type"] == "voice":
            await callback.bot.send_voice(int(forum_id), message_thread_id=topic.message_thread_id, voice=mat["file_id"])
        elif mat["type"] == "audio":
            await callback.bot.send_audio(int(forum_id), message_thread_id=topic.message_thread_id, audio=mat["file_id"])
        elif mat["type"] == "text" and mat["value"] != "Немає":
            await callback.bot.send_message(int(forum_id), message_thread_id=topic.message_thread_id, text=f"📎 <b>Матеріали (текст):</b> {mat['value']}")

    await state.clear()
    await callback.message.edit_text(f"✅ Замовлення #{order_id} передано в ІТ")
    await callback.answer()


# =========================================
# УНІВЕРСАЛЬНА ЗМІНА СТАТУСУ РОЗРОБНИКОМ
# =========================================

# =========================================
# УНІВЕРСАЛЬНА ЗМІНА СТАТУСУ РОЗРОБНИКОМ
# =========================================

@router.callback_query(F.data.startswith("set_status:"))
async def change_order_status_callback(callback: CallbackQuery, bot: Bot):
    _, order_id_str, new_status = callback.data.split(":")
    order_id = int(order_id_str)
    
    developer = callback.from_user
    dev_name = f"@{developer.username}" if developer.username else developer.full_name

    async with async_session() as session:
        res = await session.execute(select(Order).filter(Order.id == order_id))
        order = res.scalar_one_or_none()
        
        if not order:
            return await callback.answer("❌ Замовлення не знайдено в базі даних!", show_alert=True)
            
        # 🔥 ГОЛОВНЕ ВИПРАВЛЕННЯ: при натисканні "Взяти замовлення" чітко закріплюємо його за тобою!
        if new_status == "in_work":
            order.developer_id = developer.id

        order.status = new_status
        await session.commit()
        manager_id = order.user_id

    kb = InlineKeyboardBuilder()
    if new_status == "in_work":
        kb.button(text="🔄 На доопрацювання", callback_data=f"set_status:{order_id}:revision")
        kb.button(text="🏁 Завершити замовлення", callback_data=f"set_status:{order_id}:completed")
        kb.adjust(1)
        status_text = f"👨‍💻 <b>Замовлення #{order_id} взято в роботу</b>\nРозробник: {dev_name}"
    elif new_status == "revision":
        kb.button(text="🛠 Продовжити роботу", callback_data=f"set_status:{order_id}:in_work")
        kb.button(text="🏁 Завершити замовлення", callback_data=f"set_status:{order_id}:completed")
        kb.adjust(1)
        status_text = f"🔄 <b>Замовлення #{order_id} переведено на доопрацювання!</b>\nРозробник: {dev_name}"
    elif new_status == "completed":
        kb.button(text="✅ Завершено", callback_data="none")
        status_text = f"✅ <b>Замовлення #{order_id} успішно завершено!</b>\nВиконав: {dev_name}"
    else:
        status_text = f"📌 Статус замовлення #{order_id} змінено на: {new_status}\nРозробник: {dev_name}"

    try:
        await callback.message.edit_reply_markup(reply_markup=kb.as_markup())
    except Exception:
        pass

    target_chat_id = manager_id 

    if target_chat_id:
        try:
            await bot.send_message(
                chat_id=target_chat_id,
                text=status_text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Не вдалося надіслати сповіщення в чат: {e}")

    await callback.answer("Статус успішно оновлено ✅")