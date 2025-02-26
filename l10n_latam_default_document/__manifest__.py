{
    'name': 'Default Latam Document',
    'version': '18.0.1.0.0',
    'summary': 'Permite ordenar los tipos de documentos de latinoamérica para dar prioridad a un documento por defecto',
    'description': 'Default Latam Document',
    'category': 'Localization',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'license': 'LGPL-3',
    'depends': ['l10n_latam_invoice_document'],
    'data': [
        'views/l10n_latam_document_type_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
