import time
from database.db_handler import DatabaseHandler
from income_module import Income
from invoices_module import Invoices
from tax_calculator_module import TaxCalculator
from notifier_module import Notifier


def main():
    # Configuración de la base de datos y módulos
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

    # Opciones del menú
    while True:
        print("\nBienvenido a Financial Manager App")
        print("1. Añadir ingreso")
        print("2. Añadir factura")
        print("3. Añadir obligación fiscal")
        print("4. Ver ingresos")
        print("5. Ver facturas")
        print("6. Ver obligaciones fiscales")
        print("7. Notificar obligaciones fiscales próximas")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            date = input("Ingrese la fecha (YYYY-MM-DD): ")
            amount = float(input("Ingrese el monto: "))
            category = input("Ingrese la categoría (recurring/sporadic): ")
            description = input("Ingrese la descripción: ")
            income.add_income(date, amount, category, description)
            print("Ingreso añadido correctamente.")

        elif opcion == '2':
            date = input("Ingrese la fecha (YYYY-MM-DD): ")
            description = input("Ingrese la descripción: ")
            amount = float(input("Ingrese el monto: "))
            type = input("Ingrese el tipo (income/expense): ")
            invoices.add_invoice(date, description, amount, type)
            print("Factura añadida correctamente.")

        elif opcion == '3':
            date = input("Ingrese la fecha (YYYY-MM-DD): ")
            amount = float(input("Ingrese el monto: "))
            description = input("Ingrese la descripción: ")
            tax_calculator.add_tax_obligation(date, amount, description)
            print("Obligación fiscal añadida correctamente.")

        elif opcion == '4':
            ingresos = income.get_all_incomes()
            for ingreso in ingresos:
                print(ingreso)

        elif opcion == '5':
            facturas = invoices.get_all_invoices()
            for factura in facturas:
                print(factura)

        elif opcion == '6':
            obligaciones = tax_calculator.get_all_tax_obligations()
            for obligacion in obligaciones:
                print(obligacion)

        elif opcion == '7':
            notifier.notify_upcoming_tax_obligations()

        elif opcion == '8':
            print("Saliendo de la aplicación...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

    db.close_connection()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAplicación detenida por el usuario.")
