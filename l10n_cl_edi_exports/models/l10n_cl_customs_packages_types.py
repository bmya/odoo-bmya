from odoo import _, api, fields, models


class L10nCLCustomsPackagesTypes(models.Model):
    _name = 'l10n_cl.customs.packages.types'

    code = fields.Char('Code')
    name = fields.Char('Name')
    description = fields.Text('Description')
