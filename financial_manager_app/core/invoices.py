from database.db_handler import DatabaseHandler

class Invoices:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def add_invoice(self, date, description, amount, type):
        if type not in ('income', 'expense'):
            raise ValueError("El tipo de factura debe ser 'income' o 'expense'")
        self.db_handler.insert_invoice(date, description, amount, type)

    def get_all_invoices(self):
        return self.db_handler.get_all_invoices()

    def get_total_income(self):
        invoices = self.get_all_invoices()
        return sum(invoice[3] for invoice in invoices if invoice[4] == 'income')

    def get_total_expenses(self):
        invoices = self.get_all_invoices()
        return sum(invoice[3] for invoice in invoices if invoice[4] == 'expense')

    def calculate_net_balance(self):
        return self.get_total_income() - self.get_total_expenses()

# Ejemplo de uso
db = DatabaseHandler()
invoices = Invoices(db)
invoices.add_invoice("2024-10-18", "Compra de suministros", 300.0, "expense")
print(invoices.get_all_invoices())
print("Ingresos totales:", invoices.get_total_income())
print("Gastos totales:", invoices.get_total_expenses())
print("Balance neto:", invoices.calculate_net_balance())
db.close_connection()
