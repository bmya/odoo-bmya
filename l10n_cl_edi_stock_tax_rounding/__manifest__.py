{
    'name': 'Chile - Delivery Guide Tax Rounding',
    'icon': '/l10n_cl/static/description/icon.png',
    'version': '1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'author': 'Blanco Martín y Asociados SpA, ADHOC SA',
    'website': 'https://www.bmya.cl',
    'summary': 'Calcula los impuestos de la guía de despacho con el método de redondeo de la compañía',
    'description': """
La guía de despacho electrónica calcula el IVA línea por línea y suma los importes ya
redondeados, sin importar el método de redondeo configurado en la compañía. En pesos
chilenos eso hace que el IVA de la guía quede unos pesos por encima del de la orden de
venta y de la factura, que redondean globalmente.

Este módulo recalcula los totales de la guía con los mismos helpers que usan la orden de
venta y la factura, de modo que los tres documentos informen el mismo IVA. Solo actúa
cuando la compañía está configurada para redondear globalmente.
""",
    'depends': [
        'l10n_cl_edi_stock',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OPL-1',
}
