from odoo import _, api, fields, models


class L10nCLCustomsPaymentTerms(models.Model):
    _name = 'l10n_cl.customs.payment.terms'

    code = fields.Char('Code')
    name = fields.Char('Name')
    description = fields.Text('Description')
