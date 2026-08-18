import unittest

from app.keyboards.developer.dashboard import get_developer_dashboard_kb
from app.keyboards.developer.orders import get_developer_project_actions_kb


class DeveloperKeyboardTests(unittest.TestCase):
    def test_dashboard_keyboard_contains_main_sections(self):
        keyboard = get_developer_dashboard_kb()
        button_texts = [button.text for row in keyboard.inline_keyboard for button in row]

        self.assertIn("📥 Нові замовлення", button_texts)
        self.assertIn("👨‍💻 Мої проєкти", button_texts)
        self.assertIn("⏳ В роботі", button_texts)
        self.assertIn("🧪 На перевірці", button_texts)
        self.assertIn("✅ Завершені", button_texts)
        self.assertIn("📁 Архів", button_texts)
        self.assertIn("🔍 Пошук замовлення", button_texts)
        self.assertIn("💬 Чат з менеджером", button_texts)
        self.assertIn("📎 Файли проєкту", button_texts)
        self.assertIn("📊 Моя статистика", button_texts)

    def test_project_actions_keyboard_contains_full_set(self):
        keyboard = get_developer_project_actions_kb(42)
        callback_data = [button.callback_data for row in keyboard.inline_keyboard for button in row]

        self.assertIn("dev_project_view_42", callback_data)
        self.assertIn("dev_project_message_42", callback_data)
        self.assertIn("dev_project_upload_file_42", callback_data)
        self.assertIn("dev_project_upload_result_42", callback_data)
        self.assertIn("dev_project_status_42", callback_data)
        self.assertIn("dev_project_progress_42", callback_data)
        self.assertIn("dev_project_deadline_42", callback_data)
        self.assertIn("dev_project_history_42", callback_data)
        self.assertIn("dev_project_issue_42", callback_data)
        self.assertIn("dev_project_complete_42", callback_data)


if __name__ == "__main__":
    unittest.main()
