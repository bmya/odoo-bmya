{
    'name': 'Disable Vendor Bill Valuation',
    'version': '1.0',
    'summary': 'Allows disabling the revaluation of products when a vendor bill is posted with a price difference with '
               'the PO. This configuration is done in the product category.',
    'description': '',
    'category': 'Accounting',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'license': 'LGPL-3',
    'depends': ['purchase_stock'],
    'data': [
        'views/product_category_views.xml',
    ],
    'installable': True,
}
