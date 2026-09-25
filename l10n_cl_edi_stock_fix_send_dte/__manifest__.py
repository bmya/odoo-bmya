{
    'name': 'Chile - EDI Send Delivery Guides to SII',
    'icon': '/l10n_cl/static/description/icon.png',
    'version': '20.0.1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'author': 'Blanco Martín y Asociados SpA',
    'website': 'https://www.bmya.cl',
    'summary': 'Envía al SII las guías de despacho que quedaron sin informar',
    'description': """
En Odoo 20 la guía de despacho ya no se envía sola al SII: queda en "not sent" hasta
que alguien usa el botón del formulario.

Este módulo suma a l10n_cl_edi_fix_send_dte un cron horario que envía esas guías. Se
instala solo cuando están los dos, l10n_cl_edi_fix_send_dte y l10n_cl_edi_stock.
""",
    'license': 'LGPL-3',
    'depends': [
        'l10n_cl_edi_stock',
        'l10n_cl_edi_fix_send_dte',
    ],
    'data': [
        'data/cron.xml',
    ],
    'installable': True,
    'auto_install': True,
}
