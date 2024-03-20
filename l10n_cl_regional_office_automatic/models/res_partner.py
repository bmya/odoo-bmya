from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.partner'

    l10n_cl_sii_regional_office = fields.Selection(related='ref_company_ids.l10n_cl_sii_regional_office',
        readonly=False)

    @api.onchange('city_id')
    @api.depends('city_id')
    def _change_regional_office(self):
        if self.country_id != self.env.ref('base.cl'):
            return
        self.l10n_cl_sii_regional_office = self.city_id.l10n_cl_sii_regional_office
