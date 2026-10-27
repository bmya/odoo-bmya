from odoo.upgrade import util


def migrate(cr, version):
    # Vista heredada de versiones anteriores que agrega el campo
    # currency_rate_readonly (eliminado). Si queda en la BD, la validación
    # de view_account_change_currency falla durante la actualización.
    util.remove_view(cr, 'account_move_change_currency.view_account_change_no_exchange_currency')
