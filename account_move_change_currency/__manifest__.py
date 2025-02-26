{
    'author': 'Blanco Martín & Asociados, Adhoc S.A.',
    'category': 'Accounting & Finance',
    'summary': 'Este módulo permite seleccionar una moneda diferente una vez que se ha creado la factura en borrador, y al hacerlo recorre todas las lineas de la factura y actualiza la moneda y el monto utilizando la tasa previamente seleccionada.',
    'depends': ['account'],
    'name': 'Account Move Change Currency',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/account_change_currency_view.xml',
        'views/move_view.xml',
    ],
    'version': '17.0.1.0.0',
    'website': 'https://www.bmya.cl',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
