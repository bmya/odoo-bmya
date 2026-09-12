from odoo import Command
from odoo.tests import tagged

from odoo.addons.l10n_cl_edi_stock.tests.common import TestL10nClEdiStockCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
class TestDeliveryGuideTaxRounding(TestL10nClEdiStockCommon):
    """El IVA de la guía tiene que dar lo mismo que el de la orden de venta.

    Los dos productos del common dejan un IVA con decimales
    (172.050 * 19% = 32.689,5 y 51.240 * 19% = 9.735,6), así que sumar los importes
    redondeados de cada línea da 42.426 y redondear el total una sola vez da 42.425.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chilean_partner_a.l10n_cl_delivery_guide_price = 'product'
        cls.picking = cls.env['stock.picking'].create({
            'name': 'Test Delivery Guide Rounding',
            'partner_id': cls.chilean_partner_a.id,
            'location_id': cls.stock_location,
            'location_dest_id': cls.customer_location,
            'picking_type_id': cls.warehouse.out_type_id.id,
        })
        for product in (cls.product_with_taxes_a, cls.product_with_taxes_b):
            cls.env['stock.move'].create({
                'product_id': product.id,
                'product_uom': product.uom_id.id,
                'product_uom_qty': 1,
                'quantity': 1,
                'procure_method': 'make_to_stock',
                'picking_id': cls.picking.id,
                'location_id': cls.stock_location,
                'location_dest_id': cls.customer_location,
                'company_id': cls.env.company.id,
            })

    def test_delivery_guide_round_globally(self):
        self.env.company.tax_calculation_rounding_method = 'round_globally'
        amounts, __, line_amounts = self.picking._l10n_cl_get_tax_amounts()

        self.assertEqual(amounts['vat_amount'], 42425.0)
        self.assertEqual(amounts['subtotal_amount_taxable'], 223290.0)
        self.assertEqual(amounts['subtotal_amount_exempt'], 0.0)
        self.assertEqual(amounts['total_amount'], 265715.0)
        # la suma de los montos de las líneas cierra con el neto del encabezado
        self.assertEqual(
            sum(line['total_amount'] for line in line_amounts.values()),
            amounts['subtotal_amount_taxable'])

    def test_delivery_guide_round_globally_matches_sale_order(self):
        self.env.company.tax_calculation_rounding_method = 'round_globally'
        sale_order = self.env['sale.order'].create({
            'partner_id': self.chilean_partner_a.id,
            'order_line': [Command.create({
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': product.list_price,
                'tax_ids': [Command.set(self.tax_19.ids)],
            }) for product in (self.product_with_taxes_a, self.product_with_taxes_b)],
        })
        amounts, __, __ = self.picking._l10n_cl_get_tax_amounts()

        self.assertEqual(amounts['vat_amount'], sale_order.amount_tax)
        self.assertEqual(amounts['subtotal_amount_taxable'], sale_order.amount_untaxed)
        self.assertEqual(amounts['total_amount'], sale_order.amount_total)

    def test_delivery_guide_round_per_line(self):
        """Con redondeo por línea el módulo no interviene."""
        self.env.company.tax_calculation_rounding_method = 'round_per_line'
        amounts, __, __ = self.picking._l10n_cl_get_tax_amounts()

        self.assertEqual(amounts['vat_amount'], 42426.0)
        self.assertEqual(amounts['total_amount'], 265716.0)
