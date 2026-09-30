from unittest.mock import patch

from freezegun import freeze_time

from odoo.tests import tagged

from odoo.addons.l10n_cl_edi.tests.common import _check_with_xsd_patch, _is_valid_certificate

from .common import TestL10nClEdiStockFixSendDteCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
@patch('odoo.addons.certificate.models.certificate.CertificateCertificate._compute_is_valid', _is_valid_certificate)
class TestCronSendDeliveryGuide(TestL10nClEdiStockFixSendDteCommon):
    """El cron envía al SII las guías de despacho que quedaron en "not sent".

    Los tests no llegan al SII: en modo DEMO el envío solo marca el DTE como aceptado.
    """

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_sends_pending_delivery_guide(self):
        picking = self._create_delivery_guide()
        self.env.company.l10n_cl_dte_service_provider = 'SIIDEMO'
        self._trigger_cron('l10n_cl_edi_stock_fix_send_dte.ir_cron_send_dte_to_sii')
        self.assertEqual(picking.l10n_cl_dte_status, 'accepted')
