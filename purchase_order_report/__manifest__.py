# Copyright 2019 Blanco Martín & Asociados (https://www.bmya.cl).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order Report',
    'summary': """
        This module adapts the purchase order to chilean format
    """,
    'version': '1.0.0',
    'license': 'LGPL-3',
    'author': 'Blanco Martin & Asociados',
    'website': 'https://www.bmya.cl',
    'depends': [
        'purchase',
        'l10n_cl',
    ],
    'data': [
        'views/purchase_order_report.xml',
    ],
    'installable': False,
}
