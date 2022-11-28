{
    "name": """Chile - Stock Special Fields """,
    'version': '0.0.2',
    'category': 'Localization/Chile',
    'license': "OPL-1",
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'description': """
Agrega Campos Especiales en el modelo stock
===========================================
    """,
    'website': 'http://blancomartin.cl',
    'depends': [
        'l10n_cl_edi_stock',
        'delivery',
        'fleet'
    ],
    'data': [
        'views/stock_picking.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
