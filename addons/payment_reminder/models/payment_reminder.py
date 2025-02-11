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
        
        mail_template = self.env.ref('payment_reminder.mail_template_payment_reminder')
        
        for invoice in invoices:
            if invoice.partner_id.email:
                mail_template.send_mail(invoice.id, force_send=True)

class PaymentReminderCron(models.Model):
    _name = 'payment.reminder.cron'
    _description = 'Scheduled Task to Send Payment Reminders'
    
    def run_cron_task(self):
        self.env['account.move']._send_payment_reminder()