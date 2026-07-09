{
    'name': 'Chilean Edi Fix Validation',
    'version': '19.0.1.0.0',
    'summary': 'Evita rechazos por parte del SII validando campos obligatorios',
    'description': 'Evita rechazos por parte del SII por falta de algunos campos obligatorios. Inicialmente la comuna, '
                   'que se encuentra en el campo Ciudad',
    'category': 'Localization',
    'author': 'Blanco Martín y Asociados SpA',
    'website': 'https://www.bmya.cl',
    'license': 'OPL-1',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],
    'installable': True,
    'auto_install': True
}
