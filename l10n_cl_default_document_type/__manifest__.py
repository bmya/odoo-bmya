{
    "name": "Default Document Type (Chilean Localization)",
    'summary': 'Establece un tipo de documento por defecto basado en el tipo de contribuyente (consumidor final->boleta, 1ra o 2da categoria de ventas -> factura, extranjero -> factura de exportación.',
    "description": """
        Depending on the partner's taxpayer type we set the default document type to the following:
        1st or 2nd category: Factura Electrónica (33)
        End Consumer: Boleta Electrónica (39)
        Foreigner: Factura de Exportación (110)
    """,
    'version': '18.0.1.0.0',
    'category': 'Localization',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'license': 'LGPL-3',
    'depends': ['l10n_cl'],
    'installable': True,
}
