from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    qbli = fields.Char('QBLI')
