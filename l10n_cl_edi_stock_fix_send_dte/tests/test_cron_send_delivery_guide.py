from unittest.mock import patch

from freezegun import freeze_time

from odoo.tests import tagged

from odoo.addons.l10n_cl_edi.tests.common import _check_with_xsd_patch, _is_valid_certificate
from odoo.addons.l10n_cl_edi_stock.tests.common import TestL10nClEdiStockCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
@patch('odoo.addons.certificate.models.certificate.CertificateCertificate._compute_is_valid', _is_valid_certificate)
class TestCronSendDeliveryGuide(TestL10nClEdiStockCommon):
    """El cron envía al SII las guías de despacho que quedaron en "not sent".

    Los tests no llegan al SII: en modo DEMO el envío solo marca el DTE como aceptado.
    """

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_sends_pending_delivery_guide(self):
        picking = self.env['stock.picking'].create({
            'name': 'Test Delivery Guide',
            'partner_id': self.chilean_partner_a.id,
            'location_id': self.stock_location,
            'location_dest_id': self.customer_location,
            'picking_type_id': self.warehouse.out_type_id.id,
        })
        self.env['stock.move'].create({
            'product_id': self.product_with_taxes_a.id,
            'uom_id': self.product_with_taxes_a.uom_id.id,
            'product_uom_qty': 1,
            'quantity': 1,
            'procure_method': 'make_to_stock',
            'picking_id': picking.id,
            'location_id': self.stock_location,
            'location_dest_id': self.customer_location,
            'company_id': self.env.company.id,
        })
        picking.button_validate()
        picking.create_delivery_guide()
        picking.l10n_latam_document_number = 100
        picking.l10n_cl_confirm_draft_delivery_guide()
        self.assertEqual(picking.l10n_cl_dte_status, 'not_sent')

        self.env.company.l10n_cl_dte_service_provider = 'SIIDEMO'
        with self.registry_test_mode():
            self.env.ref('l10n_cl_edi_stock_fix_send_dte.ir_cron_send_dte_to_sii').method_direct_trigger()
        self.assertEqual(picking.l10n_cl_dte_status, 'accepted')
