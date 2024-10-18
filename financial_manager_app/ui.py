from flask import Flask, request, render_template, redirect, url_for
from database.db_handler import DatabaseHandler
from income_module import Income
from invoices_module import Invoices
from tax_calculator_module import TaxCalculator
from notifier_module import Notifier

app = Flask(__name__)

db = DatabaseHandler()
income = Income(db)
invoices = Invoices(db)
tax_calculator = TaxCalculator(db)

# Configuración de email para el notificador
email_config = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'username': 'tu_email@example.com',
    'password': 'tu_contraseña',
    'from_email': 'tu_email@example.com',
    'to_email': 'destinatario@example.com'
}
notifier = Notifier(db, email_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        try:
            income.add_income(date, float(amount), category, description)
            return redirect(url_for('home'))
        except ValueError as e:
            return str(e)
    return render_template('add_income.html')

@app.route('/add_invoice', methods=['GET', 'POST'])
def add_invoice():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        type = request.form['type']
        try:
            invoices.add_invoice(date, description, float(amount), type)
            return redirect(url_for('home'))
        except ValueError as e:
            return str(e)
    return render_template('add_invoice.html')

@app.route('/add_tax_obligation', methods=['GET', 'POST'])
def add_tax_obligation():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        description = request.form['description']
        try:
            tax_calculator.add_tax_obligation(date, float(amount), description)
            return redirect(url_for('home'))
        except ValueError as e:
            return str(e)
    return render_template('add_tax_obligation.html')

@app.route('/view_incomes')
def view_incomes():
    incomes = income.get_all_incomes()
    return render_template('view_incomes.html', incomes=incomes)

@app.route('/view_invoices')
def view_invoices():
    invoices_list = invoices.get_all_invoices()
    return render_template('view_invoices.html', invoices=invoices_list)

@app.route('/view_tax_obligations')
def view_tax_obligations():
    obligations = tax_calculator.get_all_tax_obligations()
    return render_template('view_tax_obligations.html', obligations=obligations)

@app.route('/notify_upcoming_tax_obligations')
def notify_upcoming_tax_obligations():
    notifier.notify_upcoming_tax_obligations()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
