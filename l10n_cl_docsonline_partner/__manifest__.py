# -*- coding: utf-8 -*-
{
    "name": """Chile get customer data from www.documentosonline.cl""",
    'version': '16.0.2.1.0',
    'category': 'Localization/Chile',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'license': 'LGPL-3',
    'summary': '',
    'depends': [
        'l10n_cl_edi',
        'l10n_cl_counties',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/res_config_settings.xml',
        'wizard/data_docsonline_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
