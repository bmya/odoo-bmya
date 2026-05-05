from odoo import api, fields, models
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_exempt = fields.Monetary(
        string="Exempt Amount",
        currency_field="company_currency_id",
        compute="_compute_amount_exempt",
        store=True,
        readonly=True,
        help="Sum of invoice line amounts that have no taxes or only 0% taxes.",
    )

    @api.depends(
        "direction_sign",
        "invoice_line_ids.balance",
        "invoice_line_ids.display_type",
        "invoice_line_ids.tax_ids",
        "invoice_line_ids.tax_ids.amount",
        "invoice_line_ids.tax_ids.amount_type",
    )
    def _compute_amount_exempt(self):
        for move in self:
            if not move.is_invoice(include_receipts=True):
                move.amount_exempt = 0.0
                continue

            exempt_total_balance = 0.0
            for line in move.invoice_line_ids.filtered(lambda l: not l.display_type):
                taxes = line.tax_ids.flatten_taxes_hierarchy().filtered(
                    lambda tax: tax.amount_type != "group"
                )
                if not taxes or all(float_is_zero(tax.amount, precision_digits=4) for tax in taxes):
                    exempt_total_balance += line.balance

            # line.balance is accounting-signed; invert to keep invoice amounts positive in lists.
            move.amount_exempt = -exempt_total_balance
