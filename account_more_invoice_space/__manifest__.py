# Copyright 2024 Blanco Martín & Asociados (https://www.bmya.cl).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'More Invoice Space',
    'summary': 'Reduces padding and margins below the header to the minimum, and reduces the font of the body to 80%.',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Blanco Martín & Asociados',
    'website': 'https://www.bmya.cl',
    'depends': [
        'account',
    ],
    'data': [
        'views/report_invoice.xml',
        'views/report_template.xml',
    ],
}
