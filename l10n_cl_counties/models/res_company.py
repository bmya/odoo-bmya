from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    real_city = fields.Char(related='partner_id.real_city', string='City')

    @api.onchange('state_id', 'city_id')
    def _change_city_province(self):
        if self.country_id != self.env.ref('base.cl'):
            return
        if self.city_id.state_id.parent_id:
            self.partner_id.state_id = self.city_id.state_id.parent_id
        if self.state_id == self.env.ref('base.state_cl_13'):
            self.real_city = 'Santiago'
            self.partner_id.real_city = 'Santiago'
        else:
            self.real_city = self.city_id.name
            self.partner_id.real_city = self.city_id.name
            self.partner_id.city = self.city_id.name
