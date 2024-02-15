from odoo import models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_valued_in_moves(self):
        stock_moves = super()._get_valued_in_moves()
        return stock_moves.filtered(lambda m: m.product_id.categ_id.reevaluate_on_bill_price_difference)
