from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_invoice_id = fields.Many2one(
        'res.partner', string='Dirección de Facturación',
        readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    def _default_invoice_partner(self):
        return self.partner_id

    def _l10n_cl_get_comuna_recep(self):
        if self.partner_invoice_id.state_id.name:
            return _format_length(self.partner_invoice_id.state_id.name)
        return super()._l10n_cl_get_comuna_recep()
