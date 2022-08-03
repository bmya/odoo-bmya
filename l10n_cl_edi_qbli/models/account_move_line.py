from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    qbli = fields.Char('QBLI')
