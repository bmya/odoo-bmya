{
    'name': 'Latam Document with Fiscal Position',
    'version': '17.0.1.0.0',
    'summary': 'Agrega una posicion fiscal enlazada a los tipos de documentos.',
    'description': '''
    When selecting the document type, is very handy, to link that document type with a fiscal position.
    For example when you use 110 document type in Chile, it is very useful to remove the VAT tax automatically,
    or for 39 document type in Chile, not to use ILA taxes.
    ''',
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
