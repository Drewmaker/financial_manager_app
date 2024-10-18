# Financial Manager App

## Descripción
Esta aplicación es una herramienta de gestión financiera que permite a los autónomos y trabajadores llevar un control efectivo de sus ingresos, gastos y obligaciones fiscales. Además, cuenta con un sistema de notificaciones que envía recordatorios sobre próximas obligaciones fiscales tanto por consola como por correo electrónico.

## Funcionalidades
- **Gestión de Facturas**: Registro de facturas de ingresos y gastos.
- **Gestión de Ingresos**: Control de ingresos recurrentes y esporádicos.
- **Cálculo de Obligaciones Fiscales**: Registra y calcula obligaciones fiscales pendientes.
- **Notificaciones**: Sistema de notificaciones que envía alertas sobre obligaciones fiscales próximas por correo electrónico.

## Requisitos
- Python 3.x
- SQLite3
- Biblioteca `smtplib` para envío de correos electrónicos
- Biblioteca `threading` para ejecutar el servicio de notificaciones en segundo plano

## Instalación
1. Clona el repositorio o descarga los archivos del proyecto.
2. Instala las dependencias ejecutando el siguiente comando:
   ```
   pip install -r requirements.txt
   ```

## Configuración
1. **Configuración de correo electrónico**: Para enviar notificaciones por correo electrónico, edita la configuración de correo en el archivo `app.py` con los detalles de tu servidor SMTP, tu correo electrónico y contraseña.

## Ejecución
Ejecuta el archivo principal para iniciar la aplicación:
```
python app.py
```

Durante la ejecución, la aplicación:
- Permitirá registrar ingresos, facturas y obligaciones fiscales.
- Enviará notificaciones sobre próximas obligaciones fiscales (tanto manualmente como automáticamente).

## Notas
- Asegúrate de proporcionar credenciales de correo válidas para que las notificaciones se envíen correctamente.
- El servicio de notificaciones automáticas se ejecuta cada 24 horas de forma predeterminada.

## Contribuciones
Las contribuciones son bienvenidas. Puedes hacer un fork del repositorio y enviar pull requests para mejoras o nuevas funcionalidades.

## Licencia
Este proyecto está bajo la Licencia MIT.

