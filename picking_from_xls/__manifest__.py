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
    'license': 'LGPL-3',
    'price': 48.00,
    'currency': 'EUR',
    'data': [
        'views/stock_picking_view.xml',
        ],
    'version': '17.0.1.0',
    'website': 'https://www.bmya.cl',
    'installable': False,
    'auto-install': False
}
