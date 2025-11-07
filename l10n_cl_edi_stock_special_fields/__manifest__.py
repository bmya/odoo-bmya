{
    "name": """Chile - Stock Special Fields """,
    'version': '19.0.1.0.0',
    'category': 'Localization/Chile',
    'license': "LGPL-3",
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'summary': 'Agrega Campos adicionales en el modelo stock como chofer, etc. utilizando el modulo de flota.',
    'description': """
Agrega Campos Especiales en el modelo stock
===========================================
    """,
    'website': 'http://blancomartin.cl',
    'depends': [
        'l10n_cl_edi_stock',
        'stock_delivery',
        'fleet'
    ],
    'data': [
        'views/stock_picking.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
