from odoo.addons.l10n_cl_edi_stock.tests.common import TestL10nClEdiStockCommon


class TestL10nClEdiStockFixSendDteCommon(TestL10nClEdiStockCommon):

    def _create_delivery_guide(self):
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
        return picking

    def _trigger_cron(self, xmlid):
        with self.registry_test_mode():
            self.env.ref(xmlid).method_direct_trigger()
