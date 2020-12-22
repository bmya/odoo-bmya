from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_country(self):
        try:
            return self.env.user.company_id.country_id or False
        except:
            return False

    country_id = fields.Many2one("res.country", default=_default_country)
    state_id = fields.Many2one("res.country.state", compute='_change_state_province', store=True, readonly=False,
        string='Ubication', domain="[('country_id', '=', country_id), ('type', '=', 'normal')]")
    real_city = fields.Char(compute='_change_real_city_province', string='City.')
    city = fields.Char(compute='_change_city_province', string='City', store=True, readonly=False)

    @api.depends('country_id', 'state_id', 'city_id')
    def _change_real_city_province(self):
        if self.country_id != self.env.ref('base.cl'):
            self.real_city = False
        if self.state_id == self.env.ref('base.state_cl_13'):
            self.real_city = 'Santiago'
        else:
            self.real_city = self.city_id.name

    @api.depends('country_id', 'state_id', 'city_id')
    def _change_city_province(self):
        if self.country_id != self.env.ref('base.cl'):
            return
        self.city = self.city_id.name

    @api.depends('country_id', 'city_id')
    def _change_state_province(self):
        if self.country_id != self.env.ref('base.cl'):
            return
        self.state_id = self.city_id.state_id.parent_id
