from odoo import _, api, fields, models


class L10nCLCustomsPorts(models.Model):
    _name = 'l10n_cl.customs.ports'

    name = fields.Char('Name')
    code = fields.Char('Code')
    country_id = fields.Many2one('res.country', string='Country')
