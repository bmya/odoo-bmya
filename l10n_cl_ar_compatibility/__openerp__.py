# -*- coding: utf-8 -*-
{
    'name': 'Chile - Localization Backward Compatibility with Argentinean Localization',
    'version': '1.0',
    'license': 'AGPL-3',
    'category': 'Chilean Localization',
    'sequence': 14,
    'summary': 'Localization, Chile, Configuration',
    'description': """Este módulo sirve para instalaciones intermedias de Chile
En donde se utilizaron antes, módulos de la localización Argentina.


afip_document_class_id->sii_document_class_id
afip_document_class_id->sii_document_number
afip_service_start->sii_service_start
afip_service_end->sii_service_end
afip_cae->sii_caf
afip_cae_due->sii_caf_status
afip_batch_number->sii_batch_number
    """,
    'author':  u'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'images': [
    ],
    'depends': [
        'account'
    ],
    'data': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
