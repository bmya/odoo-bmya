from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_invoice_id = fields.Many2one(
        'res.partner', string='Dirección de Facturación',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id), "
               "'|', ('parent_id', '=', partner_id), ('id', '=', partner_id)]", )

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.partner_invoice_id = self.partner_id

    # def _format_length(self, text, text_len):
    #     # to-do: quitar si está en edi util (en ultima version de 14.0)
    #     return text and text[:text_len] or ''

    def _default_invoice_partner(self):
        return self.partner_id

    def _l10n_cl_get_comuna_recep(self):
        if self.partner_invoice_id.state_id.name:
            return self._format_length(self.partner_invoice_id.state_id.name, 20)
        return super()._l10n_cl_get_comuna_recep()