from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.config import settings

import logging


logger = logging.getLogger("devflow")


def build_developer_offer_text(order, manager, client) -> str:
    created_at = getattr(order, "created_at", None)
    created_value = created_at.strftime("%d.%m.%Y %H:%M") if hasattr(created_at, "strftime") else str(created_at or "—")
    manager_name = getattr(manager, "full_name", None) or getattr(manager, "telegram_id", "—")
    client_name = getattr(client, "full_name", None) or getattr(client, "telegram_id", "—")
    manager_username = getattr(manager, "username", None) or "—"
    client_username = getattr(client, "username", None) or "—"

    return (
        f"🆕 <b>Новая заявка разработчикам</b>\n\n"
        f"ID заказа: {order.id}\n"
        f"Название проекта: {order.title}\n"
        f"Категория: {getattr(order, 'project_type', '—')}\n"
        f"Описание: {getattr(order, 'description', '—')}\n"
        f"Стоимость: {getattr(order, 'budget', '—')}\n"
        f"Дедлайн: {getattr(order, 'contact', '—')}\n"
        f"Менеджер: {manager_name} (@{manager_username})\n"
        f"Клиент: {client_name} (@{client_username})\n"
        f"Дата создания: {created_value}\n\n"
        f"👀 Подробнее\n"
        f"✅ Взять заказ"
    )


def build_developer_offer_keyboard(order_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="👀 Подробнее", callback_data=f"dev_view_{order_id}")
    builder.button(text="✅ Взять заказ", callback_data=f"dev_take_{order_id}")
    builder.adjust(1)
    return builder.as_markup()


def build_manager_accept_message(developer) -> str:
    developer_name = getattr(developer, "full_name", None) or getattr(developer, "telegram_id", "—")
    developer_username = getattr(developer, "username", None) or "без ника"
    developer_id = getattr(developer, "telegram_id", "—")
    return (
        f"✅ Вашу заявку на выполнение заказа принял разработчик.\n\n"
        f"👤 Разработчик: {developer_name}\n"
        f"@{developer_username}\n"
        f"ID пользователя: {developer_id}\n\n"
        f"💬 Написать разработчику"
    )


def build_developer_accept_message(manager) -> str:
    manager_name = getattr(manager, "full_name", None) or getattr(manager, "telegram_id", "—")
    manager_username = getattr(manager, "username", None) or "без ника"
    manager_id = getattr(manager, "telegram_id", "—")
    return (
        f"✅ Вы успешно приняли заказ.\n\n"
        f"📋 Менеджер: {manager_name}\n"
        f"@{manager_username}\n"
        f"ID пользователя: {manager_id}\n\n"
        f"💬 Написать менеджеру"
    )


def build_contact_keyboard(user_id: int, label: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=label, callback_data=f"contact_user_{user_id}")
    return builder.as_markup()


class ForumService:

    def __init__(
        self,
        db_session: AsyncSession,
        bot: Bot
    ):
        self.db = db_session
        self.bot = bot



    async def create_order_topic(
        self,
        order_id: int,
        title: str,
        username: str,
        description: str,
        budget: float
    ):

        try:

            # Создаём новую тему в форуме менеджеров
            topic = await self.bot.create_forum_topic(
                chat_id=settings.MANAGER_FORUM_ID,
                name=f"Заказ #{order_id} | {title}"
            )


            text = f"""
🆕 <b>Новый заказ #{order_id}</b>

👤 Клиент:
@{username}

📌 Проект:
<b>{title}</b>

📝 Описание:

{description}

💰 Бюджет:
<b>${budget}</b>

⚡ Статус:
Новый
"""


            # Первое сообщение в созданную тему
            await self.bot.send_message(
                chat_id=settings.MANAGER_FORUM_ID,
                message_thread_id=topic.message_thread_id,
                text=text,
                parse_mode=ParseMode.HTML
            )


            logger.info(
                f"Создан топик для заказа #{order_id}"
            )


            return topic.message_thread_id



        except Exception as e:

            logger.error(
                f"Ошибка создания топика заказа #{order_id}: {e}"
            )

            return None



    async def send_order_to_developer(
        self,
        order_id: int,
        description: str
    ):

        text = f"""
💻 <b>Новый заказ #{order_id}</b>

📌 Задача:

{description}
"""


        try:

            await self.bot.send_message(
                chat_id=settings.DEVELOPER_FORUM_ID,
                text=text,
                parse_mode=ParseMode.HTML
            )


            logger.info(
                f"Заказ #{order_id} отправлен разработчикам"
            )


        except Exception as e:

            logger.error(
                f"Ошибка отправки разработчику: {e}"
            )



    async def create_topic(
        self,
        title: str,
        author_id: int
    ):

        logger.info(
            f"Создана тема '{title}' от пользователя {author_id}"
        )

        return {
            "topic_id": 101,
            "title": title
        }



    async def add_post(
        self,
        topic_id: int,
        user_id: int,
        content: str
    ):

        logger.info(
            f"Сообщение в теме {topic_id}: {content}"
        )

        return True



    async def get_recent_topics(self):

        return [
            {
                "id": 1,
                "title": "Обговорення нових тарифів"
            },
            {
                "id": 2,
                "title": "Технічні питання CRM"
            }
        ]