# -*- coding: utf-8 -*-
{
    'name': 'Picking from XLS File',
    'author': 'Blanco Martín & Asociados',
    'category': 'Inventory',
    'depends': ['stock'],
    'external_dependencies': {
        'python': [
            'xlrd',
            'base64'
        ]
    },
    'license': 'OPL-1',
    'price': 48.00,
    'currency': 'EUR',
    'data': [
        'views/stock_picking_view.xml',
        ],
    'version': '1.0',
    'website': 'https://www.bmya.cl',
    'installable': True,
    'auto-install': False
}
