{
    "name": """Chile - Add QBLI Field to invoices """,
    'version': '17.0.1.0',
    'category': 'Localization/Chile',
    'license': 'LGPL-3',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'description': """
Adds QBLI to the invoice lines, according to requirements from some customers using SAP
=======================================================================================
//CdgItem/TpoCodigo
//CdgItem/VlrCodigo
    """,
    'website': 'http://bmya.cl',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'views/account_move_view.xml',
        'template/dte_template.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
