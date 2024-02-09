from odoo import models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _apply_price_difference(self):
        # Prevent valuation for Vendor Bills
        return self.env['stock.valuation.layer'].sudo(), self.env['account.move.line'].sudo()
