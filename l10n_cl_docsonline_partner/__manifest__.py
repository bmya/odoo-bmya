# -*- coding: utf-8 -*-
{
    "name": """Chile get customer data from www.documentosonline.cl""",
    'version': '17.0.1.0',
    'category': 'Localization/Chile',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'license': 'LGPL-3',
    'summary': 'Permite obtener datos tributarios de los clientes conectandose a www.documentosonline.cl. Requiere obtener una API de este sitio. Hay opción de uso gratuito.',
    'depends': [
        'l10n_cl_edi',
        'l10n_cl_counties',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir.config_parameter.xml',
        'views/partner_view.xml',
        'views/res_config_settings.xml',
        'wizard/data_docsonline_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
