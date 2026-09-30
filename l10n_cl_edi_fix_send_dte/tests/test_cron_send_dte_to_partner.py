from unittest.mock import patch

from freezegun import freeze_time

from odoo.tests import tagged

from odoo.addons.l10n_cl_edi.tests.common import _check_with_xsd_patch, _is_valid_certificate

from .common import TestL10nClEdiFixSendDteCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
@patch('odoo.addons.certificate.models.certificate.CertificateCertificate._compute_is_valid', _is_valid_certificate)
class TestCronSendDteToPartner(TestL10nClEdiFixSendDteCommon):
    """El cron envía al email DTE del cliente las facturas aceptadas con reparos."""

    def _verified_invoice(self, status):
        invoice = self._post_invoice()
        # what the SII workflow cron of l10n_cl_edi leaves once the SII has answered
        invoice.write({'l10n_cl_dte_status': status, 'l10n_cl_dte_partner_status': 'not_sent'})
        return invoice

    def _run_cron(self):
        self._trigger_cron('l10n_cl_edi_fix_send_dte.ir_cron_send_dte_to_partner')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_sends_objected_invoice(self):
        invoice = self._verified_invoice('objected')
        self._run_cron()
        self.assertEqual(invoice.l10n_cl_dte_partner_status, 'sent')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_leaves_accepted_invoice_to_the_sii_workflow(self):
        invoice = self._verified_invoice('accepted')
        self._run_cron()
        self.assertEqual(invoice.l10n_cl_dte_partner_status, 'not_sent')

    def test_cron_skips_invoice_older_than_30_days(self):
        with freeze_time('2019-10-24T20:00:00', tz_offset=3):
            invoice = self._verified_invoice('objected')
        with freeze_time('2019-12-24T20:00:00', tz_offset=3):
            self._run_cron()
        self.assertEqual(invoice.l10n_cl_dte_partner_status, 'not_sent')
