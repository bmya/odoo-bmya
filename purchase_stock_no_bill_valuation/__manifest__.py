{
    'name': 'Disable Vendor Bill Valuation',
    'version': '1.0',
    'summary': 'Disables the reevaluation of products when a vendor bill is posted with a different price than the one'
               'from the PO.',
    'description': 'The module automatically disables the reevaluation in all of the product categories but can be'
                   'configured with to work as before by setting "Reevaluate On Bill Price Difference" to True if you'
                   'still wish to reevaluate certain product categories on'
                   'the vendor bills.',
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
