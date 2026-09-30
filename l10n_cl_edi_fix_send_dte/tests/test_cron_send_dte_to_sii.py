from unittest.mock import patch

from freezegun import freeze_time

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.l10n_cl_edi.tests.common import _check_with_xsd_patch, _is_valid_certificate

from .common import TestL10nClEdiFixSendDteCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
@patch('odoo.addons.certificate.models.certificate.CertificateCertificate._compute_is_valid', _is_valid_certificate)
class TestCronSendDteToSii(TestL10nClEdiFixSendDteCommon):
    """El cron envía al SII las facturas que quedaron en "not sent".

    Los tests no llegan al SII: en modo DEMO el envío solo marca el DTE como aceptado.
    """

    def _run_cron(self):
        self.company_data['company'].l10n_cl_dte_service_provider = 'SIIDEMO'
        self._trigger_cron('l10n_cl_edi_fix_send_dte.ir_cron_send_dte_to_sii')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_sends_pending_invoice(self):
        invoice = self._post_invoice()
        self._run_cron()
        self.assertEqual(invoice.l10n_cl_dte_status, 'accepted')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_failing_invoice_does_not_block_the_others(self):
        failing_invoice = self._post_invoice()
        invoice = self._post_invoice()
        AccountMove = type(self.env['account.move'])
        send_dte_to_sii = AccountMove.l10n_cl_send_dte_to_sii

        def l10n_cl_send_dte_to_sii(move, *args, **kwargs):
            if move == failing_invoice:
                raise UserError("There is not a valid certificate for the company")
            return send_dte_to_sii(move, *args, **kwargs)

        with (
            patch.object(AccountMove, 'l10n_cl_send_dte_to_sii', l10n_cl_send_dte_to_sii),
            self.assertLogs('odoo.addons.l10n_cl_edi_fix_send_dte.models.account_move', level='ERROR'),
        ):
            self._run_cron()
        self.assertEqual(failing_invoice.l10n_cl_dte_status, 'not_sent')
        self.assertEqual(invoice.l10n_cl_dte_status, 'accepted')
