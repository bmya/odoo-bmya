# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class AccountInvoiceReference(models.Model):
    _inherit = 'account.invoice.reference'

    move_id = fields.Many2one(
        'account.invoice',
        ondelete='cascade',
        index=True,
        copy=False,
        string="Referenced Document",
    )


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_shipping_id = fields.Many2one('res.partner')
    invoice_payment_term_id = fields.Many2one('account.payment.term')
    fiscal_position_id = fields.Many2one('account.fiscal.position')
    invoice_date = fields.Date(string='Invoice date')
    invoice_date_due = fields.Date(string='Invoice date due')
    invoice_user_id = fields.Many2one('res.users')
    team_id = fields.Many2one('crm.team')
    l10n_cl_reference_ids = fields.One2many('account.invoice.reference', 'move_id', readonly=True, states={'draft': [('readonly', False)]}, )
    invoice_id = fields.Integer('invoice_id')
    l10n_cl_dte_status = fields.Char('Dte status')
    move_type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', default='entry')


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_line_id = fields.Integer()
    price_unit = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'), default=0.0)
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)
    invoice_line_tax_ids = fields.Many2many('account.tax','account_move_line_tax', 'move_line_id', 'tax_id',string='Taxes',
                                            domain=[('type_tax_use', '!=', 'none'), '|', ('active', '=', False),
                                                    ('active', '=', True)], oldname='invoice_line_tax_id')
    exclude_from_invoice_tab = fields.Boolean(default=True)
    sale_line_ids = fields.Many2many('sale.order.line')