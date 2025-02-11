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