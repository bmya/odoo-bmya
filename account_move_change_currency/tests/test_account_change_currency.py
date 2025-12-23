from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.fields import Command


class TestAccountChangeCurrency(TransactionCase):
    """Tests for changing currency on account moves"""

    def setUp(self):
        super().setUp()
        # Get company and its currency (don't change it!)
        self.company = self.env.user.company_id
        self.company_currency = self.company.currency_id

        # Get other currencies for testing
        self.currency_usd = self.env.ref('base.USD')
        self.currency_eur = self.env.ref('base.EUR')

        # Identify which currency is different from company currency
        if self.company_currency != self.currency_usd:
            self.foreign_currency = self.currency_usd
        else:
            self.foreign_currency = self.currency_eur

        # Create partner
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

        # Create account (Odoo 19 uses company_ids instead of company_id)
        self.account_receivable = self.env['account.account'].search([
            ('account_type', '=', 'asset_receivable'),
            ('company_ids', 'in', self.company.id)
        ], limit=1)

        if not self.account_receivable:
            self.account_receivable = self.env['account.account'].create({
                'name': 'Test Receivable',
                'code': 'TEST_REC',
                'account_type': 'asset_receivable',
                'company_ids': [Command.set([self.company.id])],
            })

        self.account_revenue = self.env['account.account'].search([
            ('account_type', '=', 'income'),
            ('company_ids', 'in', self.company.id)
        ], limit=1)

        if not self.account_revenue:
            self.account_revenue = self.env['account.account'].create({
                'name': 'Test Revenue',
                'code': 'TEST_REV',
                'account_type': 'income',
                'company_ids': [Command.set([self.company.id])],
            })

        # Create product
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 1000.0,
            'standard_price': 500.0,
        })

    def test_currency_rate_calculation(self):
        """Test that currency rate is calculated correctly"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': self.company_currency.id,
        })

        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.foreign_currency.id,
            'currency_rate': 1.0,  # Initial value (required field)
        })

        # Trigger onchange to recalculate rate
        wizard._onchange_currency()

        self.assertTrue(
            wizard.currency_rate > 0,
            "Currency rate should be calculated and positive"
        )
        self.assertTrue(
            wizard.inverse_currency_rate > 0,
            "Inverse currency rate should be calculated and positive"
        )

    def test_inverse_rate_calculation(self):
        """Test that inverse rate is calculated from rate"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        })

        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.foreign_currency.id,
            'currency_rate': 800.0,
        })

        wizard._onchange_currency_rate()

        self.assertAlmostEqual(
            wizard.inverse_currency_rate,
            1 / 800.0,
            places=10,
            msg="Inverse rate should be 1 / currency_rate"
        )

    def test_rate_from_inverse_calculation(self):
        """Test that rate is calculated from inverse rate"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
        })

        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.foreign_currency.id,
            'currency_rate': 1.0,  # Initial value (required field)
            'inverse_currency_rate': 0.00125,  # 1/800
        })

        # Call onchange to recalculate rate from inverse_rate
        wizard._onchange_inverse_currency_rate()

        self.assertAlmostEqual(
            wizard.currency_rate,
            800.0,
            places=5,
            msg="Rate should be 1 / inverse_currency_rate"
        )

    def test_change_currency_on_invoice(self):
        """Test changing currency updates invoice and lines"""
        # Create invoice in company currency
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': self.company_currency.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 1000.0,
                'account_id': self.account_revenue.id,
            })],
        })

        original_price = invoice.invoice_line_ids[0].price_unit

        # Change to foreign currency with rate 0.00125 (1 foreign = 800 company)
        conversion_rate = 0.00125
        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.foreign_currency.id,
            'currency_rate': conversion_rate,
        })

        wizard.change_currency()

        # Verify currency changed
        self.assertEqual(
            invoice.currency_id,
            self.foreign_currency,
            "Invoice currency should be changed to foreign currency"
        )

        # Verify price converted
        expected_price = original_price * conversion_rate
        self.assertAlmostEqual(
            invoice.invoice_line_ids[0].price_unit,
            expected_price,
            places=2,
            msg="Price should be converted using currency rate"
        )

    def test_narration_updated_with_rate_info(self):
        """Test that narration is updated with currency change info"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': self.company_currency.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 1000.0,
                'account_id': self.account_revenue.id,
            })],
        })

        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.foreign_currency.id,
            'currency_rate': 0.00125,
        })

        wizard.change_currency()

        self.assertIn(
            '||',
            invoice.narration or '',
            "Narration should contain rate information marker"
        )

    def test_same_currency_returns_early(self):
        """Test that changing to same currency returns without changes"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': self.company_currency.id,
        })

        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.company_currency.id,
            'currency_rate': 1.0,
        })

        result = wizard.change_currency()

        self.assertEqual(
            result['type'],
            'ir.actions.act_window_close',
            "Should close window when currency is the same"
        )
        self.assertEqual(
            invoice.currency_id,
            self.company_currency,
            "Currency should remain unchanged"
        )

    def test_no_invoice_in_context_raises_error(self):
        """Test that missing invoice in context raises ValidationError"""
        with self.assertRaises(ValidationError) as context:
            wizard = self.env['account.change.currency'].create({
                'currency_id': self.foreign_currency.id,
                'currency_rate': 800.0,
            })
            wizard._get_move()

        self.assertIn(
            'active_id',
            str(context.exception).lower(),
            "Error should mention missing active_id"
        )

    def test_all_invoice_lines_updated(self):
        """Test that all invoice lines are updated when changing currency"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': self.company_currency.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price_unit': 1000.0,
                    'account_id': self.account_revenue.id,
                }),
                (0, 0, {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price_unit': 2000.0,
                    'account_id': self.account_revenue.id,
                }),
            ],
        })

        wizard = self.env['account.change.currency'].with_context(
            active_id=invoice.id
        ).create({
            'currency_id': self.foreign_currency.id,
            'currency_rate': 0.00125,
        })

        wizard.change_currency()

        # Check all lines have new currency
        for line in invoice.invoice_line_ids:
            self.assertEqual(
                line.currency_id,
                self.foreign_currency,
                "All invoice lines should have new currency"
            )
