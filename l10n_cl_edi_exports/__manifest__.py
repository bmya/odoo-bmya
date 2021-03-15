{
    "name": """Chile - Enable Exports """,
    'version': '1.0.',
    'category': 'Localization/Chile',
    "license": "LGPL-3",
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'description': """
Agrega Campos Necesarios para Exportaciones XML
===============================================
    """,
    'website': 'http://blancomartin.cl',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'template/dte_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
