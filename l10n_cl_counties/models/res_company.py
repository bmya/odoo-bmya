from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    real_city = fields.Char(related='partner_id.real_city', string='City.')
    city_id = fields.Many2one('res.city', related='partner_id.city_id', readonly=False)
