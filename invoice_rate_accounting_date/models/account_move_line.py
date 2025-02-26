from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_rate_date(self):
        self.ensure_one()
        return self.move_id.date or self.move_id.invoice_date or fields.Date.context_today(self)
