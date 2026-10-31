{
    'name': 'Chile - EDI N/C a facturas de compra (46)',
    'version': '19.0.1.0.0',
    'category': 'Localization/Chile',
    'license': 'LGPL-3',
    'icon': '/account/static/description/l10n.png',
    'sequence': 12,
    'author': 'Blanco Martín y Asociados SpA',
    'summary': 'Emite y envía al SII la nota de crédito (61) de una factura de compra (46).',
    'description': """
La factura de compra (46) la emite la empresa, y su nota de crédito también. Odoo trata esa
nota de crédito (61, en el diario de compras) como un documento recibido: no la timbra ni la
envía al SII, y si el proveedor es extranjero ni siquiera deja elegir el tipo 61.

Este módulo:

- ofrece la 61 en el wizard de reversa y en una N/C nueva cuando el proveedor es extranjero;
- deja pasar la validación «You need a journal without the use of documents for foreign
  suppliers» cuando la N/C referencia una 46;
- numera la N/C con la secuencia del CAF 61, compartida con las N/C de venta;
- genera el DTE al validarla, para que lo envíe el cron o el botón «Send Now to SII».
""",
    'website': 'https://www.bmya.cl',
    'depends': [
        'l10n_cl_edi',
    ],
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}
