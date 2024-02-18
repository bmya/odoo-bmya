{
    "name": """Chile - Legacy Special Fields """,
    'version': '17.0.1.0',
    'category': 'Localization/Chile',
    'license': 'LGPL-3',
    'icon': '/l10n_cl_partner_extra_xml_identification/static/description/icon.png',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'description': """
    Permite emitir la factura a la sucursal de un cliente, y asignar la deuda directamente al cliente real.
    Este módulo se conserva para mantener la compatibilidad con versiones anteriores, pero desde odoo 16 este problema
    puede ser resuelto sin módulos adicionales.
    """,
    'website': 'http://blancomartin.cl',
    'depends': [
        'l10n_cl_partner_extra_xml_identification',
    ],
    'data': [
        'views/account_move_view.xml',
        'template/dte_template.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
