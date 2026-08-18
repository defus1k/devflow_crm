# services/salary_service.py

class SalaryService:
    def __init__(self, db_session):
        self.db = db_session

    async def calculate_monthly_bonus(self, employee_id: int):
        """
        Розрахунок бонусу на основі кількості закритих угод.
        """
        # Логіка: отримати кількість угод з бази даних
        closed_deals = 10  # Припустимо, ми отримали це з БД
        bonus_per_deal = 500.00
        
        total_bonus = closed_deals * bonus_per_deal
        return total_bonus

    async def generate_salary_report(self, employee_id: int):
        """
        Формування звіту про зарплату за місяць.
        """
        base_salary = 20000.00
        bonus = await self.calculate_monthly_bonus(employee_id)
        
        return {
            "base": base_salary,
            "bonus": bonus,
            "total": base_salary + bonus
        }