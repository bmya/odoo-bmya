# Copyright 2024 Blanco Martín & Asociados (https://www.bmya.cl).

{
    'name': 'Invoice Rate from Accounting Date',
    'summary': 'Odoo hizo un cambio en el código para que la fecha de la tasa que se usa en facturas, sea la fecha de factura y no la fecha contable, lo que generó múltiples problemas. Este módulo soluciona eso dando precedencia a la fecha contable.',
    'description': 'Accounting date takes precedence over the invoice date for the currencie\'s exchange rate',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'depends': [
        'account',
    ],
    'data': [
    ],
    'installable': True,
}
