# Copyright (c) 2019 - Blanco Martín & Asociados. https://www.bmya.cl
{
    'name': 'Chile - Expenses Fix',
    'version': "17.0.1.0",
    'license': 'LGPL-3',
    'description': """
Chilean expenses fix. When installing hr_expense application it fixes the Journal Type to allow registration of
expenses in miscellaneous Journals.
    """,
    'author': 'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'hr_expense',
        'l10n_cl',
    ],
    'active': True,
    'auto_install': True,
    'installable': False,
}
