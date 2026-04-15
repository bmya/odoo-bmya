from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('l10n_latam_document_type_id')
    def _update_fiscal_position(self):
        for move in self:
            if not move.l10n_latam_document_type_id.fiscal_position_id:
                continue
            move.fiscal_position_id = move.l10n_latam_document_type_id.fiscal_position_id

    @api.model
    def create(self, vals):
        record = super(AccountMove, self).create(vals)
        record._update_fiscal_position()
        return record
