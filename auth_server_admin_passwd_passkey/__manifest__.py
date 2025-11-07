# -*- encoding: utf-8 -*-
{
    'name': 'Authentification - Admin Passkey',
    'version': '19.0.1.0.0',
    'category': 'base',
    'summary': 'Módulo que permite que en servidores el administrador del servidor se identifique como representante de cualquier usuario, con fines de servicio técnico. Cada ingreso queda identificado en la plataforma',
    'description': """
Server Admin password become a passkey for all active logins
============================================================

Functionality :
---------------
* You can now login with any user using server admin password
(admin_passwd parameter) or with admin user password (superuser password)
    """,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends': [
        'base',
        ],
    'data': [
    ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'installable': False,
    'auto_install': False,
}
