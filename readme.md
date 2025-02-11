# Automatización de Envío de Recordatorios

## Descripción del Proceso Automatizado
Se ha desarrollado un módulo en Odoo que envía automáticamente recordatorios de pago a los clientes con facturas vencidas en los próximos tres días. Este proceso ayuda a mejorar la gestión de cobros y evitar retrasos en los pagos.

## Requisitos Funcionales y No Funcionales

### Funcionales:
- Identificar facturas con fecha de vencimiento dentro de los próximos tres días.
- Enviar correos electrónicos automáticos a los clientes con recordatorio de pago.
- Utilizar una plantilla de correo predefinida.

### No Funcionales:
- La automatización debe ejecutarse como una tarea programada en Odoo.
- El sistema debe verificar que el cliente tenga un correo registrado antes de enviar el recordatorio.
- La solución debe ser escalable y fácil de modificar.

## Pasos Seguidos en el Desarrollo
1. **Extender el modelo `account.move`** para agregar la función `_send_payment_reminder`.
2. **Buscar facturas con vencimiento en los próximos tres días y estado no pagado**.
3. **Verificar que el cliente tenga un correo electrónico registrado**.
4. **Enviar el correo utilizando una plantilla predefinida**.
5. **Crear una tarea programada (`cron job`) para ejecutar la función periódicamente**.

## Ejemplo de Código

```python
from odoo import models, fields, api
from datetime import datetime, timedelta

class PaymentReminder(models.Model):
    _inherit = 'account.move'

    def _send_payment_reminder(self):
        today = datetime.today().date()
        invoices = self.search([
            ('invoice_date_due', '<=', today + timedelta(days=3)),
            ('payment_state', '!=', 'paid')
        ])
        
        mail_template = self.env.ref('mail_template_payment_reminder')
        
        for invoice in invoices:
            if invoice.partner_id.email:
                mail_template.send_mail(invoice.id, force_send=True)
```

## Resultados de las Pruebas Realizadas
- Se probó la ejecución manual de la función `_send_payment_reminder` y se verificó que las facturas correctas fueron seleccionadas.
- Se validó que los correos electrónicos fueron enviados solo a clientes con correos registrados.
- Se configuró la tarea programada y se comprobó su ejecución en el tiempo esperado.

## Conclusiones y Posibles Mejoras
- La automatización mejora la eficiencia en la gestión de cobros.
- Se podría agregar una opción para personalizar los días de anticipación del recordatorio.
- Se podría implementar una vista en la interfaz de usuario para gestionar los recordatorios enviados.

