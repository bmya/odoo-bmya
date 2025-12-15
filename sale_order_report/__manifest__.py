# Copyright 2019 Blanco Martín & Asociados (https://www.bmya.cl).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Order Report',
    'summary': """Este modulo modifica el formato de las ordenes de venta para adaptarse a los formatos chilenos (recuadro margen superior derecho).""",
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'depends': [
        'sale',
        'l10n_cl',
    ],
    'data': [
        'views/sale_order_report.xml',
    ],
    'installable': False,
}
