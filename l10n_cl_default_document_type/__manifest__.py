{
    "name": "Default Document Type (Chilean Localization)",
    'summary': 'Automatically set a document type depending on the customer\'s taxpayer type.',
    "description": """
        Depending on the partner's taxpayer type we set the default document type to the following:
        1st or 2nd category: Factura Electrónica (33)
        End Consumer: Boleta Electrónica (39)
        Foreigner: Factura de Exportación (110)
    """,
    'version': '17.0.1.0',
    'category': 'Localization',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'license': 'LGPL-3',
    'depends': ['l10n_cl'],
    'installable': False,
    'auto_install': False
}
