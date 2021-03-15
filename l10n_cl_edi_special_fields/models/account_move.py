from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'account.move'

    invoice_partner_id = fields.Many2one('res.partner', default=lambda self: self._default_invoice_partner(),
                                         string='Dirección de Facturación', required=True)

    def _default_invoice_partner(self):
        return self.partner_id

    def _l10n_cl_get_comuna_recep(self):
        if self.invoice_partner_id.state_id.name:
            return _format_length(self.invoice_partner_id.state_id.name)
        return super()._l10n_cl_get_comuna_recep()
