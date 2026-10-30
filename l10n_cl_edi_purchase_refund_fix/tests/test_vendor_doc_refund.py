import base64
from unittest.mock import patch

from freezegun import freeze_time
from lxml import etree

from odoo.exceptions import ValidationError
from odoo.tests import Form, tagged
from odoo.tools import misc, os

from odoo.addons.l10n_cl_edi.tests.common import TestL10nClEdiCommon, _check_with_xsd_patch

NS = {'ns0': 'http://www.sii.cl/SiiDte'}


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
class TestVendorDocRefund(TestL10nClEdiCommon):
    """ N/C (61) emitida sobre una factura de compra (46).

    La 46 la emite la empresa, así que su N/C también: tiene que salir con folio del CAF 61,
    compartido con las N/C de venta, y con DTE para enviar al SII. """

    @classmethod
    @patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
    def setUpClass(cls, chart_template_ref='cl'):
        super().setUpClass(chart_template_ref=chart_template_ref)
        company = cls.company_data['company']
        cls.doc_46 = cls.env.ref('l10n_cl.dc_fc_f_dte')
        cls.doc_61 = cls.env.ref('l10n_cl.dc_nc_f_dte')
        cls.doc_33 = cls.env.ref('l10n_cl.dc_a_f_dte')

        caf_file_template = misc.file_open(os.path.join(
            'l10n_cl_edi', 'tests', 'template', 'caf_file_template.xml')).read()
        for doc_type in (cls.doc_46, cls.doc_61):
            caf_file = caf_file_template.replace('<TD></TD>', '<TD>%s</TD>' % doc_type.code)
            cls.env['l10n_cl.dte.caf'].sudo().create({
                'filename': 'FoliosSII76201224%s21201910221946.xml' % doc_type.code,
                'caf_file': base64.b64encode(caf_file.encode('utf-8')),
                'l10n_latam_document_type_id': doc_type.id,
                'status': 'in_use',
            })

        cls.purchase_journal = cls.env['account.journal'].create({
            'name': 'Purchase Journal Test',
            'type': 'purchase',
            'code': 'BILL2',
            'l10n_latam_use_documents': True,
        })
        chart = cls.env['account.chart.template'].with_company(company)
        cls.tax_iva_purchase = chart.ref('OTAX_19')
        cls.tax_iva_withholding = chart.ref('I_RTI')
        cls.tax_iva_sale = chart.ref('ITAX_19')

        cls.partner_foreign = cls.env['res.partner'].create({
            'name': 'Digital Services Inc.',
            'is_company': True,
            'street': '1 Market St',
            'city': 'San Francisco',
            'country_id': cls.env.ref('base.us').id,
            'l10n_cl_sii_taxpayer_type': '4',
            'l10n_cl_activity_description': 'digital services',
            'vat': '123456789',
            'l10n_cl_dte_email': 'billing@digital.example',
        })

    def _create_purchase_invoice_46(self, partner):
        invoice = self.env['account.move'].with_context(default_move_type='in_invoice').create({
            'partner_id': partner.id,
            'move_type': 'in_invoice',
            'invoice_date': '2019-10-23',
            'invoice_date_due': '2019-10-23',
            'journal_id': self.purchase_journal.id,
            'l10n_latam_document_type_id': self.doc_46.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Servicio digital',
                'product_id': self.product_a.id,
                'quantity': 1,
                'price_unit': 100000.0,
                'tax_ids': [(6, 0, (self.tax_iva_purchase | self.tax_iva_withholding).ids)],
            })],
        })
        invoice.with_context(skip_xsd=True).action_post()
        self.assertEqual(invoice.l10n_cl_dte_status, 'not_sent')
        return invoice

    def _reversal_wizard(self, move):
        return self.env['account.move.reversal'].with_context(
            active_model='account.move', active_ids=move.ids).create({
                'reason': 'Anula factura de compra',
                'journal_id': move.journal_id.id,
            })

    def _refund(self, move):
        wizard = self._reversal_wizard(move)
        refund = self.env['account.move'].browse(wizard.refund_moves()['res_id'])
        refund.with_context(skip_xsd=True).action_post()
        return refund

    def _dte_tree(self, move):
        return etree.fromstring(base64.b64decode(move.l10n_cl_sii_send_file.datas))

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_refund_chilean_supplier_generates_dte(self):
        invoice = self._create_purchase_invoice_46(self.partner_sii)
        wizard = self._reversal_wizard(invoice)
        self.assertEqual(wizard.l10n_latam_document_type_id, self.doc_61)
        self.assertFalse(wizard.l10n_latam_manual_document_number)

        refund = self.env['account.move'].browse(wizard.refund_moves()['res_id'])
        refund.with_context(skip_xsd=True).action_post()

        self.assertEqual(refund.move_type, 'in_refund')
        self.assertTrue(refund.l10n_cl_is_vendor_doc_refund)
        self.assertEqual(refund.name, 'N/C 000001')
        self.assertEqual(refund.l10n_cl_dte_status, 'not_sent')
        self.assertTrue(refund.l10n_cl_dte_file)

        dte = self._dte_tree(refund)
        self.assertEqual(dte.findtext('.//ns0:IdDoc/ns0:TipoDTE', namespaces=NS), '61')
        self.assertEqual(dte.findtext('.//ns0:Referencia/ns0:TpoDocRef', namespaces=NS), '46')
        self.assertEqual(dte.findtext('.//ns0:Referencia/ns0:FolioRef', namespaces=NS),
                         invoice.l10n_latam_document_number)
        self.assertEqual(dte.findtext('.//ns0:Totales/ns0:MntNeto', namespaces=NS), '100000')
        self.assertEqual(dte.findtext('.//ns0:Totales/ns0:IVA', namespaces=NS), '19000')
        self.assertEqual(dte.findtext('.//ns0:ImptoReten/ns0:TipoImp', namespaces=NS), '15')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_refund_foreign_supplier(self):
        invoice = self._create_purchase_invoice_46(self.partner_foreign)
        wizard = self._reversal_wizard(invoice)
        self.assertEqual(wizard.l10n_latam_available_document_type_ids._origin, self.doc_61)
        self.assertEqual(wizard.l10n_latam_document_type_id, self.doc_61)

        refund = self.env['account.move'].browse(wizard.refund_moves()['res_id'])
        refund.with_context(skip_xsd=True).action_post()

        self.assertEqual(refund.state, 'posted')
        self.assertEqual(refund.l10n_cl_dte_status, 'not_sent')
        dte = self._dte_tree(refund)
        self.assertEqual(dte.findtext('.//ns0:Receptor/ns0:RUTRecep', namespaces=NS), '55555555-5')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_sale_and_purchase_refunds_share_caf_61(self):
        out_invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create({
            'partner_id': self.partner_sii.id,
            'move_type': 'out_invoice',
            'invoice_date': '2019-10-23',
            'invoice_date_due': '2019-10-23',
            'journal_id': self.sale_journal.id,
            'l10n_latam_document_type_id': self.doc_33.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_a.id,
                'quantity': 1,
                'price_unit': 50000.0,
                'tax_ids': [(6, 0, self.tax_iva_sale.ids)],
            })],
        })
        out_invoice.with_context(skip_xsd=True).action_post()
        out_refund = self._refund(out_invoice)
        purchase_refund = self._refund(self._create_purchase_invoice_46(self.partner_sii))
        next_out_refund = self._refund(out_invoice)

        self.assertEqual(
            [out_refund.name, purchase_refund.name, next_out_refund.name],
            ['N/C 000001', 'N/C 000002', 'N/C 000003'])

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_new_credit_note_foreign_supplier(self):
        invoice = self._create_purchase_invoice_46(self.partner_foreign)
        refund_form = Form(self.env['account.move'].with_context(default_move_type='in_refund'))
        refund_form.journal_id = self.purchase_journal
        refund_form.partner_id = self.partner_foreign
        refund_form.invoice_date = '2019-10-23'
        self.assertEqual(refund_form.l10n_latam_available_document_type_ids[:], self.doc_61)
        refund_form.l10n_latam_document_type_id = self.doc_61
        with refund_form.l10n_cl_reference_ids.new() as reference:
            reference.origin_doc_number = invoice.l10n_latam_document_number
            reference.l10n_cl_reference_doc_type_id = self.doc_46
            reference.reference_doc_code = '1'
            reference.reason = 'Anula factura de compra'
            reference.date = invoice.invoice_date
        self.assertFalse(refund_form.l10n_latam_manual_document_number)
        # Primera 61 de la secuencia: l10n_latam pide el folio inicial, como en una N/C de venta
        refund_form.l10n_latam_document_number = '1'
        with refund_form.invoice_line_ids.new() as line:
            line.product_id = self.product_a
            line.price_unit = 100000.0
            line.tax_ids.clear()
        refund = refund_form.save()

        refund.with_context(skip_xsd=True).action_post()
        self.assertTrue(refund.l10n_cl_is_vendor_doc_refund)
        self.assertEqual(refund.name, 'N/C 000001')
        self.assertEqual(refund.l10n_cl_dte_status, 'not_sent')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_foreign_credit_note_without_46_reference_is_rejected(self):
        refund = self.env['account.move'].with_context(default_move_type='in_refund').create({
            'partner_id': self.partner_foreign.id,
            'move_type': 'in_refund',
            'invoice_date': '2019-10-23',
            'journal_id': self.purchase_journal.id,
            'l10n_latam_document_type_id': self.doc_61.id,
            'l10n_latam_document_number': '7',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_a.id,
                'price_unit': 1000.0,
                'tax_ids': [],
            })],
        })
        with self.assertRaises(ValidationError):
            refund.with_context(skip_xsd=True).action_post()

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_received_credit_note_stays_manual(self):
        refund = self.env['account.move'].with_context(default_move_type='in_refund').create({
            'partner_id': self.partner_sii.id,
            'move_type': 'in_refund',
            'invoice_date': '2019-10-23',
            'journal_id': self.purchase_journal.id,
            'l10n_latam_document_type_id': self.doc_61.id,
            'l10n_latam_document_number': '555',
            'l10n_cl_reference_ids': [(0, 0, {
                'origin_doc_number': '123',
                'l10n_cl_reference_doc_type_id': self.doc_33.id,
                'reference_doc_code': '1',
                'reason': 'Anula factura',
                'date': '2019-10-20',
            })],
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_a.id,
                'quantity': 1,
                'price_unit': 1000.0,
                'tax_ids': [(6, 0, self.tax_iva_purchase.ids)],
            })],
        })
        self.assertTrue(refund.l10n_latam_manual_document_number)
        refund.with_context(skip_xsd=True).action_post()
        self.assertFalse(refund.l10n_cl_is_vendor_doc_refund)
        self.assertEqual(refund.name, 'N/C 000555')
        self.assertFalse(refund.l10n_cl_dte_status)
