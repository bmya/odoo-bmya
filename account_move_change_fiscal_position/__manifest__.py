{
    'name': 'Recalc Taxes with Fiscal Position',
    'version': '17.0.1.0',
    'category': 'Invoicing',
    'summary': 'En Odoo stándard, si se cambia la posición fiscal una vez que las lineas están configuradas, los impuestos permanecen inmutables. Este módulo permite que al cambiar la posición fiscal en la factura (de venta o de compra) se actualicen los impuestos en las líneas',
    'description': """
Fixes the need of taxes recalculation when fiscal position is changed.
Also, moves the fiscal position selector to main view of the invoice
    """,
    'author': 'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'license': 'LGPL-3',
    'depends': [
        'account',
        ],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
