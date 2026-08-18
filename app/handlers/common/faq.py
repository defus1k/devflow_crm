from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Словник з питаннями та відповідями
FAQ_DATA = {
    "Як створити замовлення?": "Натиснути кнопку створити замовлення у головному меню.",
    "Як вивести кошти?": "Зайдіть у 'Особистий кабінет' -> 'Вивести'.",
    "Які терміни виконання?": "Кожен проект оцінюється індивідуально після заповнення заявки.",
    "Як відбувається оплата?": 
        "Оплата замовлення відбувається у декілька етапів:\n"
        "1. Після створення заявки ми формуємо рахунок.\n"
        "2. Ви оплачуєте замовлення через реквізити.\n"
        "3. Статус вашого платежу оновлюется після перевірки адміністрації і додається вам в особистий кабінет"
    # ...
}

# Обработка нажатия кнопки "Найчастіші питання" в главном меню
@router.message(F.text == "❓ Найчастіші питання")
async def faq_menu_message(message: types.Message):
    builder = InlineKeyboardBuilder()
    for question in FAQ_DATA.keys():
        builder.button(text=question, callback_data=f"faq_{question}")
    
    builder.adjust(1) # Кнопки в один стовпчик
    await message.answer("Оберіть питання, яке вас цікавить:", reply_markup=builder.as_markup())

# Обработка выбора конкретного вопроса
@router.callback_query(F.data.startswith("faq_"))
async def process_faq(callback: types.CallbackQuery):
    question = callback.data.split("faq_")[1]
    answer = FAQ_DATA.get(question, "Відповідь не знайдена.")
    
    await callback.answer() 
    await callback.message.edit_text(
        f"❓ **{question}**\n\n💡 {answer}", 
        parse_mode="Markdown"
    )