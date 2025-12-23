from odoo.tests.common import TransactionCase
from odoo.fields import Command


class TestDefaultDocumentType(TransactionCase):
    """Tests for automatic document type assignment based on taxpayer type"""

    def setUp(self):
        super().setUp()
        # Set up Chilean company
        self.company_cl = self.env.user.company_id
        self.company_cl.country_id = self.env.ref('base.cl')

        # Get document types using XML IDs from l10n_cl data
        self.doc_type_33 = self.env.ref('l10n_cl.dc_a_f_dte', raise_if_not_found=False)  # Factura Electrónica (33)
        self.doc_type_39 = self.env.ref('l10n_cl.dc_b_f_dte', raise_if_not_found=False)  # Boleta Electrónica (39)
        self.doc_type_110 = self.env.ref('l10n_cl.dc_fe_dte', raise_if_not_found=False)  # Factura de Exportación (110)
        self.doc_type_46 = self.env.ref('l10n_cl.dc_fc_f_dte', raise_if_not_found=False)  # Factura de Compra Electrónica (46)

        # Use demo partners with valid RUTs from l10n_cl
        # Try to get demo partners, if not available create with valid RUTs
        self.partner_first_category = self.env.ref('l10n_cl.demo_partner_cl_1', raise_if_not_found=False)
        if not self.partner_first_category:
            self.partner_first_category = self.env['res.partner'].create({
                'name': 'Partner 1st Category',
                'country_id': self.env.ref('base.cl').id,
                'l10n_cl_sii_taxpayer_type': '1',
                'vat': '77594500-1',
            })

        self.partner_second_category = self.env.ref('l10n_cl.demo_partner_cl_fee_receipts', raise_if_not_found=False)
        if not self.partner_second_category:
            self.partner_second_category = self.env['res.partner'].create({
                'name': 'Partner 2nd Category',
                'country_id': self.env.ref('base.cl').id,
                'l10n_cl_sii_taxpayer_type': '2',
                'vat': '13009922-K',
            })

        # Create end consumer (type 3) with valid RUT
        self.partner_end_consumer = self.env['res.partner'].create({
            'name': 'End Consumer',
            'country_id': self.env.ref('base.cl').id,
            'l10n_cl_sii_taxpayer_type': '3',
            'vat': '12533840-2',
        })

        # Use foreign partner from base demo data
        self.partner_foreigner = self.env.ref('base.res_partner_2', raise_if_not_found=False)
        if not self.partner_foreigner:
            self.partner_foreigner = self.env['res.partner'].create({
                'name': 'Foreign Partner',
                'country_id': self.env.ref('base.us').id,
                'l10n_cl_sii_taxpayer_type': '4',
            })

        # Create journal with LATAM documents enabled
        self.journal = self.env['account.journal'].search([
            ('type', '=', 'sale'),
            ('company_id', '=', self.company_cl.id),
            ('l10n_latam_use_documents', '=', True),
        ], limit=1)

        if not self.journal:
            self.journal = self.env['account.journal'].create({
                'name': 'Test Sales Journal',
                'type': 'sale',
                'code': 'TSJ',
                'company_id': self.company_cl.id,
                'l10n_latam_use_documents': True,
            })

        # Create account for invoices (Odoo 19 uses company_ids instead of company_id)
        self.account_receivable = self.env['account.account'].search([
            ('account_type', '=', 'asset_receivable'),
            ('company_ids', 'in', self.company_cl.id)
        ], limit=1)

        if not self.account_receivable:
            self.account_receivable = self.env['account.account'].create({
                'name': 'Test Receivable',
                'code': 'TEST_REC',
                'account_type': 'asset_receivable',
                'company_ids': [Command.set([self.company_cl.id])],
            })

    def test_first_category_gets_electronic_invoice_33(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_first_category.id,
            'journal_id': self.journal.id,
            'invoice_date': '2025-01-15',
        })

        # Trigger available document types computation first
        invoice._compute_l10n_latam_available_document_types()
        invoice._compute_l10n_latam_document_type()

        self.assertTrue(
            invoice.l10n_latam_document_type_id,
            f"Document type should be set. Available: {invoice.l10n_latam_available_document_type_ids.mapped('code')}"
        )
        self.assertEqual(
            invoice.l10n_latam_document_type_id.code,
            '33',
            "1st category partner should get Factura Electrónica (33)"
        )

    def test_second_category_gets_electronic_invoice_33(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_second_category.id,
            'journal_id': self.journal.id,
            'invoice_date': '2025-01-15',
        })

        invoice._compute_l10n_latam_available_document_types()
        invoice._compute_l10n_latam_document_type()

        self.assertTrue(
            invoice.l10n_latam_document_type_id,
            "Document type should be set"
        )
        self.assertEqual(
            invoice.l10n_latam_document_type_id.code,
            '33',
            "2nd category partner should get Factura Electrónica (33)"
        )

    def test_end_consumer_gets_electronic_receipt(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_end_consumer.id,
            'journal_id': self.journal.id,
            'invoice_date': '2025-01-15',
        })

        invoice._compute_l10n_latam_available_document_types()
        invoice._compute_l10n_latam_document_type()

        self.assertTrue(
            invoice.l10n_latam_document_type_id,
            "Document type should be set"
        )
        self.assertEqual(
            invoice.l10n_latam_document_type_id.code,
            '39',
            "End consumer should get Boleta Electrónica (39)"
        )

    def test_foreigner_gets_exports_invoice110(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_foreigner.id,
            'journal_id': self.journal.id,
            'invoice_date': '2025-01-15',
        })

        invoice._compute_l10n_latam_available_document_types()
        invoice._compute_l10n_latam_document_type()

        self.assertTrue(
            invoice.l10n_latam_document_type_id,
            "Document type should be set"
        )
        self.assertEqual(
            invoice.l10n_latam_document_type_id.code,
            '110',
            "Foreign partner should get Factura de Exportación (110)"
        )

    def test_vendor_bill_first_category_gets_46(self):
        purchase_journal = self.env['account.journal'].search([
            ('type', '=', 'purchase'),
            ('company_id', '=', self.company_cl.id),
            ('l10n_latam_use_documents', '=', True),
        ], limit=1)

        if not purchase_journal:
            purchase_journal = self.env['account.journal'].create({
                'name': 'Test Purchase Journal',
                'type': 'purchase',
                'code': 'TPJ',
                'company_id': self.company_cl.id,
                'l10n_latam_use_documents': True,
            })

        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_first_category.id,
            'journal_id': purchase_journal.id,
            'invoice_date': '2025-01-15',
        })

        bill._compute_l10n_latam_available_document_types()
        bill._compute_l10n_latam_document_type()

        self.assertTrue(
            bill.l10n_latam_document_type_id,
            "Document type should be set"
        )
        self.assertEqual(
            bill.l10n_latam_document_type_id.code,
            '46',
            "Vendor bill for 1st category should get Factura de Compra Electrónica (46)"
        )
