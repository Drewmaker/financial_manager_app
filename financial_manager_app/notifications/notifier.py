import time
from datetime import datetime, timedelta
from database.db_handler import DatabaseHandler
from income_module import Income
from invoices_module import Invoices
from tax_calculator_module import TaxCalculator
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Notifier:
    def __init__(self, db_handler: DatabaseHandler, email_config: dict):
        self.db_handler = db_handler
        self.email_config = email_config

    def get_upcoming_tax_obligations(self, days_ahead=7):
        upcoming_obligations = []
        current_date = datetime.now().date()
        upcoming_date = current_date + timedelta(days=days_ahead)
        all_obligations = self.db_handler.get_all_tax_obligations()

        for obligation in all_obligations:
            obligation_date = datetime.strptime(obligation[1], "%Y-%m-%d").date()
            if current_date <= obligation_date <= upcoming_date and obligation[4] == 'pending':
                upcoming_obligations.append(obligation)
        
        return upcoming_obligations

    def notify_upcoming_tax_obligations(self):
        upcoming_obligations = self.get_upcoming_tax_obligations()
        if upcoming_obligations:
            for obligation in upcoming_obligations:
                message = f"Recordatorio: La obligación fiscal '{obligation[3]}' de {obligation[2]}€ vence el {obligation[1]}."
                print(message)
                self.send_email_notification(message)
        else:
            print("No hay obligaciones fiscales próximas en los próximos días.")

    def start_notification_service(self, interval=86400):
        def notification_loop():
            while True:
                self.notify_upcoming_tax_obligations()
                time.sleep(interval)
        
        threading.Thread(target=notification_loop, daemon=True).start()

    def send_email_notification(self, message):
        try:
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = "Recordatorio de Obligación Fiscal"
            msg.attach(MIMEText(message, 'plain'))
            
            server.send_message(msg)
            server.quit()
            print("Notificación por correo enviada exitosamente.")
        except Exception as e:
            print(f"Error al enviar notificación por correo: {e}")

# Ejemplo de uso
db = DatabaseHandler()
income = Income(db)
invoices = Invoices(db)
tax_calculator = TaxCalculator(db)

email_config = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'username': 'tu_email@example.com',
    'password': 'tu_contraseña',
    'from_email': 'tu_email@example.com',
    'to_email': 'destinatario@example.com'
}

notifier = Notifier(db, email_config)

# Añadir ingresos, facturas y obligaciones fiscales
income.add_income("2024-10-18", 2000.0, "recurring", "Salario mensual")
invoices.add_invoice("2024-10-18", "Compra de suministros", 300.0, "expense")
tax_calculator.add_tax_obligation("2024-12-31", 500.0, "Pago trimestral IRPF")

# Notificar manualmente las obligaciones fiscales próximas
notifier.notify_upcoming_tax_obligations()

# Iniciar el servicio de notificaciones automáticas (cada 24 horas)
notifier.start_notification_service()

# Mantener el programa corriendo para observar las notificaciones
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Servicio de notificaciones detenido.")
db.close_connection()
