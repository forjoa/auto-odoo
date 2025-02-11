# Automatización de Envío de Recordatorios

## Descripción del Proceso Automatizado
Este módulo de Odoo envía automáticamente recordatorios de pago a los clientes que tienen facturas con vencimiento en los próximos tres días. Su objetivo es mejorar la gestión de cobros y evitar retrasos en los pagos, notificando a los clientes de manera oportuna.

## Requisitos Funcionales y No Funcionales

### Funcionales:
- Identifica facturas con fecha de vencimiento dentro de los próximos tres días.
- Envía correos electrónicos automáticos a los clientes con un recordatorio de pago.
- Utiliza una plantilla de correo predefinida para los mensajes.

### No Funcionales:
- La automatización se ejecuta como una tarea programada en Odoo (cron job).
- El sistema verifica que el cliente tenga un correo electrónico registrado antes de enviar el recordatorio.
- La solución es escalable y fácil de modificar.

## Pasos Seguidos en el Desarrollo
1. **Extensión del modelo `account.move`:** Se agregó la función `_send_payment_reminder` para gestionar el envío de recordatorios.
2. **Búsqueda de facturas:** Se identifican las facturas con vencimiento en los próximos tres días y que no estén pagadas.
3. **Verificación de correo electrónico:** Se asegura que el cliente tenga un correo electrónico registrado antes de enviar el recordatorio.
4. **Envío de correos:** Se utiliza una plantilla de correo predefinida para enviar los recordatorios.
5. **Tarea programada:** Se creó un cron job para ejecutar la función periódicamente.

## Ejemplo de Código
```python
from odoo import models, api
from datetime import datetime, timedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _send_payment_reminder(self):
        today = datetime.today().date()
        invoices = self.search([
            ('invoice_date_due', '>=', today),
            ('invoice_date_due', '<=', today + timedelta(days=3)),
            ('payment_state', '!=', 'paid')
        ])
        
        mail_template = self.env.ref('payment_reminder.mail_template_payment_reminder')
        
        for invoice in invoices:
            if invoice.partner_id.email:
                mail_template.send_mail(invoice.id, force_send=True)
```

## Resultados de las Pruebas Realizadas
- Se verificó que la función selecciona correctamente las facturas con vencimiento en los próximos tres días.

- Se comprobó que los correos electrónicos se envían solo a clientes con correos registrados.

- La tarea programada se ejecuta en el intervalo de tiempo configurado.

## Conclusiones y Posibles Mejoras
- El módulo mejora significativamente la eficiencia en la gestión de cobros.

- En el futuro, se podría agregar una opción para personalizar los días de anticipación del recordatorio.

- También se podría implementar una vista en la interfaz de usuario para gestionar los recordatorios enviados.