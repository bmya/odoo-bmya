from odoo.tools.sql import column_exists, create_column

from . import models


def pre_init_hook(env):
    """ Crea la columna antes de que el ORM la calcule para todo account.move.

    Las N/C a una 46 que ya existen se numeraron a mano: si quedaran marcadas entrarían en la
    secuencia del CAF 61 y la desordenarían. """
    if not column_exists(env.cr, 'account_move', 'l10n_cl_is_vendor_doc_refund'):
        create_column(env.cr, 'account_move', 'l10n_cl_is_vendor_doc_refund', 'boolean')
