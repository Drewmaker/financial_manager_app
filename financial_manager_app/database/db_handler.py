import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="financial_manager.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Crear tabla de facturas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
            )
        ''')
        
        # Crear tabla de ingresos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL CHECK(category IN ('recurring', 'sporadic')),
                description TEXT
            )
        ''')

        # Crear tabla de obligaciones fiscales
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_obligations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL,
                description TEXT,
                status TEXT NOT NULL CHECK(status IN ('pending', 'paid'))
            )
        ''')

        self.connection.commit()

    def insert_invoice(self, date, description, amount, type):
        self.cursor.execute('''
            INSERT INTO invoices (date, description, amount, type) 
            VALUES (?, ?, ?, ?)
        ''', (date, description, amount, type))
        self.connection.commit()

    def insert_income(self, date, amount, category, description):
        self.cursor.execute('''
            INSERT INTO incomes (date, amount, category, description) 
            VALUES (?, ?, ?, ?)
        ''', (date, amount, category, description))
        self.connection.commit()

    def insert_tax_obligation(self, date, amount, description, status):
        self.cursor.execute('''
            INSERT INTO tax_obligations (date, amount, description, status) 
            VALUES (?, ?, ?, ?)
        ''', (date, amount, description, status))
        self.connection.commit()

    def get_all_invoices(self):
        self.cursor.execute('SELECT * FROM invoices')
        return self.cursor.fetchall()

    def get_all_incomes(self):
        self.cursor.execute('SELECT * FROM incomes')
        return self.cursor.fetchall()

    def get_all_tax_obligations(self):
        self.cursor.execute('SELECT * FROM tax_obligations')
        return self.cursor.fetchall()

    def get_pending_tax_obligations(self):
        self.cursor.execute('SELECT * FROM tax_obligations WHERE status = "pending"')
        return self.cursor.fetchall()

    def calculate_net_income(self):
        # Calcular ingresos netos: ingresos totales - gastos totales
        self.cursor.execute('SELECT SUM(amount) FROM invoices WHERE type = "income"')
        total_income = self.cursor.fetchone()[0] or 0.0
        self.cursor.execute('SELECT SUM(amount) FROM invoices WHERE type = "expense"')
        total_expenses = self.cursor.fetchone()[0] or 0.0
        return total_income - total_expenses

    def calculate_tax_due(self):
        # Calcular el total de obligaciones fiscales pendientes
        self.cursor.execute('SELECT SUM(amount) FROM tax_obligations WHERE status = "pending"')
        total_tax_due = self.cursor.fetchone()[0] or 0.0
        return total_tax_due

    def close_connection(self):
        self.connection.close()

# Ejemplo de uso
db = DatabaseHandler()
db.insert_invoice("2024-10-18", "Factura cliente A", 1000.0, "income")
db.insert_income("2024-10-18", 2000.0, "recurring", "Salario mensual")
db.insert_tax_obligation("2024-12-31", 500.0, "Pago trimestral IRPF", "pending")
print(db.get_all_invoices())
print(db.get_all_incomes())
print(db.get_all_tax_obligations())
print(db.get_pending_tax_obligations())
print("Ingresos netos:", db.calculate_net_income())
print("Obligaciones fiscales pendientes:", db.calculate_tax_due())
db.close_connection()
