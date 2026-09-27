import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _cron_l10n_cl_send_dte_to_sii(self):
        """Send to the SII the delivery guides that are still pending.

        Each guide is committed as soon as the SII answers: the upload cannot be
        rolled back, so a later failure must not discard its track id.
        """
        domain = [('l10n_cl_dte_status', '=', 'not_sent')]
        pickings = self.search(domain, order='id')
        self.env['ir.cron']._commit_progress(remaining=len(pickings))
        for picking in pickings:
            try:
                # skips the guides being sent right now from the form
                picking_to_send = picking.try_lock_for_update().filtered_domain(domain)
                if picking_to_send:
                    picking_to_send.with_company(picking_to_send.company_id).with_context(
                        cron_skip_connection_errs=True,
                    ).l10n_cl_send_dte_to_sii()
            except Exception:  # noqa: BLE001
                self.env['ir.cron']._rollback_progress()
                _logger.exception("Failed to send the delivery guide %s to the SII", picking.display_name)
            if not self.env['ir.cron']._commit_progress(1):
                break

    @api.model
    def _cron_l10n_cl_send_dte_to_partner(self):
        """Send to the partner's DTE email the delivery guides accepted by the SII.

        The SII workflow cron of l10n_cl_edi_stock checks their status without sending
        them to the partner, and the "Verify on SII" button, which does, is gone once
        the SII has answered.

        Guides older than 30 days are left out, so that installing the module does not
        email the partners the backlog that Odoo never sent.
        """
        domain = [
            ('l10n_cl_dte_status', 'in', ['accepted', 'objected']),
            ('l10n_cl_dte_partner_status', '=', 'not_sent'),
            '|',
            ('partner_id.l10n_cl_dte_email', '!=', False),
            ('partner_id.commercial_partner_id.l10n_cl_dte_email', '!=', False),
            ('date_done', '>=', 'now -30d'),
        ]
        pickings = self.search(domain, order='id')
        self.env['ir.cron']._commit_progress(remaining=len(pickings))
        for picking in pickings:
            try:
                picking_to_send = picking.try_lock_for_update().filtered_domain(domain)
                if picking_to_send:
                    picking_to_send.with_company(picking_to_send.company_id)._l10n_cl_send_dte_to_partner()
            except Exception:  # noqa: BLE001
                self.env['ir.cron']._rollback_progress()
                _logger.exception("Failed to send the delivery guide %s to the partner", picking.display_name)
            if not self.env['ir.cron']._commit_progress(1):
                break
