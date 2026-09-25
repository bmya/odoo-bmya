{
    'name': 'Chile - EDI Send DTE to SII',
    'icon': '/l10n_cl/static/description/icon.png',
    'version': '20.0.1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'author': 'Blanco Martín y Asociados SpA',
    'website': 'https://www.bmya.cl',
    'summary': 'Envía al SII los DTE contables que quedaron sin informar',
    'description': """
En Odoo 20 el XML del DTE se genera al confirmar el documento, pero el envío al SII
quedó como una opción del wizard de envío. Si el operador no la marca, la factura queda
contabilizada y el SII no la recibe.

Este módulo vuelve a enviar esos DTE: un cron horario recorre los asientos en estado
"not sent" (facturas, notas de crédito y débito, facturas de compra y, con
l10n_cl_edi_factoring, las cesiones), y la factura recupera el botón de envío manual.

Las guías de despacho las cubre l10n_cl_edi_stock_fix_send_dte, que se instala solo
cuando también está l10n_cl_edi_stock.
""",
    'license': 'LGPL-3',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'data/cron.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
