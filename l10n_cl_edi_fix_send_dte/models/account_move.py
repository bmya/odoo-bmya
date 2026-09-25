import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _cron_l10n_cl_send_dte_to_sii(self):
        """Send to the SII the DTEs posted without going through the Send wizard.

        Each document is committed as soon as the SII answers: the upload cannot be
        rolled back, so a later failure must not discard its track id.
        """
        domain = [('l10n_cl_dte_status', '=', 'not_sent')]
        moves = self.search(domain, order='id')
        self.env['ir.cron']._commit_progress(remaining=len(moves))
        for move in moves:
            try:
                # skips the documents being sent right now from the wizard or the form
                move_to_send = move.try_lock_for_update().filtered_domain(domain)
                if move_to_send:
                    move_to_send.with_company(move_to_send.company_id).with_context(
                        cron_skip_connection_errs=True,
                    ).l10n_cl_send_dte_to_sii()
            except Exception:  # noqa: BLE001
                self.env['ir.cron']._rollback_progress()
                _logger.exception("Failed to send the DTE of %s to the SII", move.display_name)
            if not self.env['ir.cron']._commit_progress(1):
                break
