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

    @api.model
    def _cron_l10n_cl_send_dte_to_partner(self):
        """Send to the partner's DTE email the DTEs accepted with objections by the SII.

        The SII workflow cron of l10n_cl_edi sends only the accepted ones, and the
        "Verify on SII" button, which sends both, is gone once the SII has answered.
        The accepted ones are left to that cron: it does not lock the documents, so
        both sending the same DTE could email it twice.

        Documents older than 30 days are left out, so that installing the module does
        not email the partners the backlog that Odoo never sent.
        """
        domain = [
            ('l10n_cl_dte_status', '=', 'objected'),
            ('l10n_cl_dte_partner_status', '=', 'not_sent'),
            ('partner_id.country_id.code', '=', 'CL'),
            '|',
            ('partner_id.l10n_cl_dte_email', '!=', False),
            ('commercial_partner_id.l10n_cl_dte_email', '!=', False),
            ('invoice_date', '>=', 'today -30d'),
        ]
        moves = self.search(domain, order='id')
        self.env['ir.cron']._commit_progress(remaining=len(moves))
        for move in moves:
            try:
                move_to_send = move.try_lock_for_update().filtered_domain(domain)
                if move_to_send:
                    move_to_send.with_company(move_to_send.company_id)._l10n_cl_send_dte_to_partner()
            except Exception:  # noqa: BLE001
                self.env['ir.cron']._rollback_progress()
                _logger.exception("Failed to send the DTE of %s to the partner", move.display_name)
            if not self.env['ir.cron']._commit_progress(1):
                break
