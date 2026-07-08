from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    l10n_cl_account_type = fields.Selection([
        ('1', 'View Account'),
        ('2', 'Savings Account'),
        ('3', 'Current Account'),
        ('4', 'RUT Account'),
    ], string='Account Type', default='3')

    bmya_preferred_payment_journal_id = fields.Many2one(
        'account.journal', string='Preferred Journal',
        domain=[('type', 'in', ('bank', 'cash', 'credit'))]
    )
