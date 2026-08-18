import logging
from alembic.config import Config
from alembic import command
import os

class MigrationManager:
    """
    Клас-обгортка для запуску міграцій через Alembic.
    Дозволяє програмно керувати версіями БД при старті бота.
    """
    def __init__(self, alembic_ini_path: str = "alembic.ini"):
        self.alembic_cfg = Config(alembic_ini_path)
        self.logger = logging.getLogger(__name__)

    def upgrade(self, revision: str = "head"):
        """
        Оновлює базу даних до вказаної ревізії (за замовчуванням — остання).
        """
        try:
            self.logger.info(f"Запуск міграцій БД до ревізії: {revision}")
            command.upgrade(self.alembic_cfg, revision)
            self.logger.info("Міграції успішно застосовані.")
        except Exception as e:
            self.logger.error(f"Помилка при застосуванні міграцій: {e}")
            raise

    def downgrade(self, revision: str):
        """
        Відкат бази даних до вказаної ревізії.
        """
        try:
            self.logger.info(f"Відкат БД до ревізії: {revision}")
            command.downgrade(self.alembic_cfg, revision)
            self.logger.info("Відкат виконано успішно.")
        except Exception as e:
            self.logger.error(f"Помилка при відкаті міграцій: {e}")
            raise

    def stamp(self, revision: str = "head"):
        """
        Позначає базу даних як таку, що знаходиться на певній версії,
        без фактичного виконання SQL-команд.
        """
        command.stamp(self.alembic_cfg, revision)

# Приклад того, як це інтегрувати в main.py:
# if __name__ == "__main__":
#     manager = MigrationManager()
#     manager.upgrade()