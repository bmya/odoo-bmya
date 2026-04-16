{
    'name': 'Chile - EDI TpoTranVenta Fix',
    'version': '19.0.1.0.0',
    'category': 'Localization/Chile',
    'license': 'LGPL-3',
    'icon': '/account/static/description/l10n.png',
    'sequence': 12,
    'author': 'Blanco Martín y Asociados',
    'summary': 'Agrega el campo TpoTranVenta al DTE según el tipo de actividad de venta.',
    'description': """
    Agrega el tag <TpoTranVenta> al XML del DTE para documentos que no son boletas ni exportaciones.
    El valor se determina automáticamente según el tipo de cuentas contables usadas en la factura:
    - 1: Ventas del giro (por defecto)
    - 2: Ventas de activo fijo
    - 3: Otras ventas
    """,
    'website': 'http://www.bmya.cl',
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
