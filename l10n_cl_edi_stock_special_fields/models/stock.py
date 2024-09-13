from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'StockPicking'

    vehicle = fields.Many2one(
        'fleet.vehicle',
        string="Vehículo",
        readonly=False,
    )
    chofer = fields.Many2one(
        'res.partner',
        string="Chofer",
        readonly=False,
    )
    patente = fields.Char(
        string="Patente",
        readonly=False,
    )
    contact_id = fields.Many2one(
        'res.partner',
        string="Contacto",
        readonly=False,
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
        readonly=False,
    )
