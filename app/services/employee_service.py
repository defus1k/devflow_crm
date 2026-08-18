# services/employee_service.py

class EmployeeService:
    def __init__(self, db_session):
        self.db = db_session

    async def add_employee(self, telegram_id: int, name: str, role: str):
        """
        Логіка додавання працівника до бази даних.
        """
        # Тут буде запит до бази даних (наприклад, через SQLAlchemy)
        print(f"Додаємо працівника {name} з роллю {role} (ID: {telegram_id})")
        return True

    async def get_employee_by_id(self, telegram_id: int):
        """
        Перевірка прав доступу працівника.
        """
        # Повертає дані працівника, якщо він є в системі
        return {"id": telegram_id, "role": "admin"}

    async def list_all_employees(self):
        """
        Виведення списку всіх працівників.
        """
        return ["Менеджер Іван", "Менеджер Олена"]