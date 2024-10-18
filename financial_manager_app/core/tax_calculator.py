from database.db_handler import DatabaseHandler

class TaxCalculator:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def add_tax_obligation(self, date, amount, description, status="pending"):
        if status not in ('pending', 'paid'):
            raise ValueError("El estado de la obligación debe ser 'pending' o 'paid'")
        self.db_handler.insert_tax_obligation(date, amount, description, status)

    def get_all_tax_obligations(self):
        return self.db_handler.get_all_tax_obligations()

    def get_pending_tax_obligations(self):
        return self.db_handler.get_pending_tax_obligations()

    def get_total_tax_due(self):
        pending_obligations = self.get_pending_tax_obligations()
        return sum(obligation[2] for obligation in pending_obligations)

    def mark_tax_as_paid(self, tax_id):
        self.db_handler.cursor.execute('''
            UPDATE tax_obligations
            SET status = 'paid'
            WHERE id = ?
        ''', (tax_id,))
        self.db_handler.connection.commit()

# Ejemplo de uso
db = DatabaseHandler()
tax_calculator = TaxCalculator(db)
tax_calculator.add_tax_obligation("2024-12-31", 500.0, "Pago trimestral IRPF")
print(tax_calculator.get_all_tax_obligations())
print("Obligaciones fiscales pendientes:", tax_calculator.get_pending_tax_obligations())
print("Total de obligaciones fiscales pendientes:", tax_calculator.get_total_tax_due())
tax_calculator.mark_tax_as_paid(1)
print("Obligaciones fiscales después de marcar como pagadas:", tax_calculator.get_all_tax_obligations())
db.close_connection()
