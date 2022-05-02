from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'StockPicking'

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

