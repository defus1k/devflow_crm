from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from app.keyboards.client.menu import get_main_menu_kb
from app.keyboards.client.support import (
    get_support_menu_kb,
    get_packages_kb,
    get_back_to_support_kb
)

router = Router()

# 1. Відкриття головного розділу по кнопці з головного меню
@router.message(F.text == "🛠 Послуги та підтримка")
async def open_support_section(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛠 <b>Відділ послуг та підтримки</b>\n\n"
        "Оберіть потрібний розділ нижче:",
        reply_markup=get_support_menu_kb(),
        parse_mode="HTML"
    )

# 2. Перегляд пакетів обслуговування
@router.callback_query(F.data == "support_packages")
async def show_maintenance_packages(callback: types.CallbackQuery):
    text = (
        "📦 <b>ПАКЕТИ ОБСЛУГОВУВАННЯ БОТА</b>\n\n"
        "🥉 <b>START — Базова підтримка</b>\n"
        "💰 <b>500 грн/міс</b>\n\n"
        "✅ Контроль роботи бота\n"
        "✅ Виправлення дрібних помилок\n"
        "✅ Перевірка сервера\n"
        "✅ Оновлення залежностей\n"
        "✅ Резервне копіювання\n\n"
        "──────────────────\n\n"
        "🥈 <b>PRO — Повне супроводження</b>\n"
        "💰 <b>1200 грн/міс</b>\n\n"
        "✅ Все з START\n"
        "✅ Швидке виправлення проблем\n"
        "✅ Моніторинг роботи\n"
        "✅ Оптимізація швидкості\n"
        "✅ Додавання невеликих змін\n\n"
        "──────────────────\n\n"
        "🥇 <b>BUSINESS — Максимальний захист</b>\n"
        "💰 <b>2500 грн/міс</b>\n\n"
        "✅ Все з PRO\n"
        "✅ Пріоритетна підтримка\n"
        "✅ Нові невеликі функції\n"
        "✅ Налаштування безпеки\n"
        "✅ Консультації по розвитку"
    )
    await callback.message.edit_text(text, reply_markup=get_packages_kb(), parse_mode="HTML")
    await callback.answer()

# 3. Додаткові послуги
@router.callback_query(F.data == "support_extra")
async def show_extra_services(callback: types.CallbackQuery):
    text = (
        "➕ <b>Додаткові послуги</b>\n\n"
        "Тут ви можете замовити разові доопрацювання, підключення платіжних систем, бази даних або зміну логіки існуючого функціоналу.\n\n"
        "Для замовлення натисніть кнопку зв'язку з менеджером. @adm_nexora_botforge"
    )
    await callback.message.edit_text(text, reply_markup=get_back_to_support_kb(), parse_mode="HTML")
    await callback.answer()

# 4. Замовити нову функцію (виправлено помилку \з)
@router.callback_query(F.data == "support_new_feature")
async def order_new_feature(callback: types.CallbackQuery):
    text = (
        "🚀 <b>Замовити нову функцію</b>\n\n"
        "Маєте ідею, як покращити свого бота? Опишіть її детально та надішліть нашому менеджеру @adm_nexora_botforge, і ми розрахуємо вартість і терміни реалізації."
    )
    await callback.message.edit_text(text, reply_markup=get_back_to_support_kb(), parse_mode="HTML")
    await callback.answer()

# 5. Зв'язатися з менеджером / Замовити пакет
@router.callback_query(F.data.in_({"support_manager", "order_package_request"}))
async def contact_manager(callback: types.CallbackQuery):
    text = (
        "📞 <b>Зв'язок з менеджером</b>\n\n"
        "З питань підключення пакетів або замовлення послуг звертайтесь до адміністратора:\n"
        "👤 Наш менеджер: @adm_nexora_botforge"
    )
    await callback.message.edit_text(text, reply_markup=get_back_to_support_kb(), parse_mode="HTML")
    await callback.answer()

# 6. Кнопка "Назад" у головне меню розділу підтримки
@router.callback_query(F.data == "back_to_support_menu")
async def back_to_support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🛠 <b>Відділ послуг та підтримки</b>\n\n"
        "Оберіть потрібний розділ нижче:",
        reply_markup=get_support_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

# 7. Повернення у загальне головне меню бота
@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("🏠 Головне меню:", reply_markup=get_main_menu_kb())
    await callback.answer()