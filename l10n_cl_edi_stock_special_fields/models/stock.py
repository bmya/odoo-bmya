from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'StockPicking'

    @api.onchange('currency_id', 'move_lines', 'l10n_cl_delivery_guide_reason')
    def _get_amount_untaxed(self):
        if not self.origin or self.l10n_cl_delivery_guide_reason == '5' or not self.move_ids_without_package:
            return 0
        total_amount_tax = 0
        sale = self.env['sale.order'].search([('name', '=', self.origin)])
        invoice_line_ids = sale.invoice_ids and sale.invoice_ids.mapped('invoice_line_ids') or False
        for stock_move_line in self.move_ids_without_package:
            if invoice_line_ids:
                invoice_line = invoice_line_ids.filtered(lambda l: l.product_id.id == stock_move_line.product_id.id)
                total_amount_tax += invoice_line._get_price_total_and_subtotal(quantity=stock_move_line.quantity_done)['price_subtotal']
        return total_amount_tax

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id.currency_id.id,
        tracking=True,
    )

    vehicle = fields.Many2one(
        'fleet.vehicle',
        string="Vehículo",
        readonly=False,
        states={'done': [('readonly', True)]},
    )
    chofer = fields.Many2one(
        'res.partner',
        string="Chofer",
        readonly=False,
        states={'done': [('readonly', True)]},
    )
    patente = fields.Char(
        string="Patente",
        readonly=False,
        states={'done': [('readonly', True)]},
    )
    contact_id = fields.Many2one(
        'res.partner',
        string="Contacto",
        readonly=False,
        states={'done': [('readonly', True)]},
    )

    transport_type = fields.Selection(
        [
            ('2', 'Despacho por cuenta de empresa'),
            ('1', 'Despacho por cuenta del cliente'),
            ('3', 'Despacho Externo'),
            ('0', 'Sin Definir')
        ],
        string="Tipo de Despacho",
        default="3",
        readonly=False, states={'done': [('readonly', True)]},
    )
