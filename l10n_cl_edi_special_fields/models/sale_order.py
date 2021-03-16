from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['partner_id'] = self.partner_id.id
        invoice_vals['partner_invoice_id'] = self.partner_invoice_id.id
        return invoice_vals
