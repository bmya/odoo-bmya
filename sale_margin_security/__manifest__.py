{
    'name': 'Sale Margin Security',
    'version': '1.0',
    'summary': 'Allows to restrict the vision of the margin in order lines',
    'description': 'Allows to restrict the vision of the margin in order lines',
    'category': 'Sale',
    'author': 'Blanco Martin y Asociados',
    'website': 'https://www.bmya.cl',
    'license': 'LGPL-3',
    'depends': ['sale_margin'],
    'data': [
        'security/sale_margin_security.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
