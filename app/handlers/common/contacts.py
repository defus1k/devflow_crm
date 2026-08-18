from aiogram import Router, types
from aiogram import F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(Command("contacts"))
@router.message(F.text == "📞 Контакти")
async def cmd_contacts(message: types.Message):
    """
    Виводить контактну інформацію компанії.
    """
    text = (
        "📞 **Наші контакти**\n\n"
        "Маєте питання чи пропозиції? Зв'яжіться з нами:\n\n"
        "🌐 ТГК: https://t.me/+uVcTH7HqRGI5MWYy\n"
        "💬 Telegram-адміністрації: @adm_nexora_botforge\n"
        
    )
    
    # Створюємо кнопку для переходу на сайт
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти в ТГК", url="https://t.me/+uVcTH7HqRGI5MWYy")
    
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")