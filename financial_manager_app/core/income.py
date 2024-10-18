from database.db_handler import DatabaseHandler

class Income:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def add_income(self, date, amount, category, description=""):
        if category not in ('recurring', 'sporadic'):
            raise ValueError("La categoría de ingreso debe ser 'recurring' o 'sporadic'")
        self.db_handler.insert_income(date, amount, category, description)

    def get_all_incomes(self):
        return self.db_handler.get_all_incomes()

    def get_total_recurring_income(self):
        incomes = self.get_all_incomes()
        return sum(income[2] for income in incomes if income[3] == 'recurring')

    def get_total_sporadic_income(self):
        incomes = self.get_all_incomes()
        return sum(income[2] for income in incomes if income[3] == 'sporadic')

    def get_total_income(self):
        incomes = self.get_all_incomes()
        return sum(income[2] for income in incomes)

# Ejemplo de uso
db = DatabaseHandler()
income = Income(db)
income.add_income("2024-10-18", 2000.0, "recurring", "Salario mensual")
print(income.get_all_incomes())
print("Ingreso total recurrente:", income.get_total_recurring_income())
print("Ingreso total esporádico:", income.get_total_sporadic_income())
print("Ingreso total:", income.get_total_income())
db.close_connection()
