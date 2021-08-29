from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('fiscal_position_id')
    def _onchange_fiscal_position(self):
        self.ensure_one()
        # only line with taxes are adjusted
        for line in self.invoice_line_ids.filtered(lambda l: not l.display_type and l.tax_ids):
            if line.product_id:
                account_id = line._get_computed_account()
                product_id = line.with_company(self.company_id).product_id
                product_tax_ids = product_id.taxes_id.filtered(lambda tax: tax.company_id == self.company_id)
                if self.move_type in ['in_invoice', 'in_refund']:
                    product_tax_ids = product_id.supplier_taxes_id.filtered(lambda x: x.company_id == self.company_id)
                if product_tax_ids:
                    tax_ids = product_tax_ids
                elif account_id.tax_ids:
                    tax_ids = account_id.tax_ids.filtered(lambda y: y.company_id == self.company_id)
                else:
                    if self.move_type in ['in_invoice', 'in_refund']:
                        tax_ids = self.company_id.account_purchase_tax_id
                    else:
                        tax_ids = self.company_id.account_sale_tax_id
                if self.fiscal_position_id:
                    tax_ids = self.fiscal_position_id.map_tax(tax_ids)
                line.tax_ids = [[6, 0, tax_ids.ids]]
                line.account_id = account_id.id
        self._recompute_tax_lines()
        self._recompute_dynamic_lines(recompute_tax_base_amount=True)
