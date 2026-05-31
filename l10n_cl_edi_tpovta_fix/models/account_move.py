from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _l10n_cl_sale_activity(self):
        account_lines = self.env['account.move.line']._read_group(
            domain=[
                ('move_id', '=', self.id),
                ('tax_line_id', '=', False),
                ('account_type', 'not in', ['asset_receivable', False])
            ],
            groupby=['account_id']
        )[0][0]
        income_line_types = account_lines.mapped('account_type')
        if 'asset_fixed' in income_line_types and 'income' not in income_line_types:
            return 2
        elif 'income' not in income_line_types and 'income_other' in income_line_types:
            return 3
        else:
            return 1
