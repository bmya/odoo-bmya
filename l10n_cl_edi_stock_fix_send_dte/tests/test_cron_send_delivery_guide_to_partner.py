from unittest.mock import patch

from freezegun import freeze_time

from odoo.tests import tagged

from odoo.addons.l10n_cl_edi.tests.common import _check_with_xsd_patch, _is_valid_certificate

from .common import TestL10nClEdiStockFixSendDteCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
@patch('odoo.addons.certificate.models.certificate.CertificateCertificate._compute_is_valid', _is_valid_certificate)
class TestCronSendDeliveryGuideToPartner(TestL10nClEdiStockFixSendDteCommon):
    """El cron envía al email DTE del cliente las guías de despacho aceptadas."""

    def _accepted_delivery_guide(self):
        picking = self._create_delivery_guide()
        # what the SII workflow cron of l10n_cl_edi_stock leaves once the SII has answered
        picking.write({'l10n_cl_dte_status': 'accepted', 'l10n_cl_dte_partner_status': 'not_sent'})
        return picking

    def _run_cron(self):
        self._trigger_cron('l10n_cl_edi_stock_fix_send_dte.ir_cron_send_dte_to_partner')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_sends_accepted_delivery_guide(self):
        picking = self._accepted_delivery_guide()
        self._run_cron()
        self.assertEqual(picking.l10n_cl_dte_partner_status, 'sent')
        mail = self.env['mail.mail'].search([('model', '=', 'stock.picking'), ('res_id', '=', picking.id)])
        self.assertEqual(mail.email_to, self.chilean_partner_a.l10n_cl_dte_email)

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_skips_partner_without_dte_email(self):
        picking = self._accepted_delivery_guide()
        self.chilean_partner_a.l10n_cl_dte_email = False
        self._run_cron()
        self.assertEqual(picking.l10n_cl_dte_partner_status, 'not_sent')

    def test_cron_skips_delivery_guide_older_than_30_days(self):
        with freeze_time('2019-10-24T20:00:00', tz_offset=3):
            picking = self._accepted_delivery_guide()
        with freeze_time('2019-12-24T20:00:00', tz_offset=3):
            self._run_cron()
        self.assertEqual(picking.l10n_cl_dte_partner_status, 'not_sent')
