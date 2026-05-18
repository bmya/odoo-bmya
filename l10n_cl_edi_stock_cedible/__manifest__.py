{
    'name': 'Chile - E-Invoicing Delivery Guide Cedible',
    'icon': '/l10n_cl/static/description/icon.png',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations/Reporting',
    'author': 'Blanco Martín & Asociados',
    'summary': 'Módulo que permite la impresión de la guía de despacho cedible como un documento separado.',
    'description': """
        E-Invoicing Delivery Guide Cedible for Chile
    """,
    'depends': [
        'l10n_cl_edi_stock',
    ],
    'data': [
        'templates/report_delivery_guide.xml',
    ],
    'installable': True,
    'auto_install': True,
    'website': 'http://www.bmya.cl',
    'license': "LGPL-3",
}
