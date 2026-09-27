from odoo import Command

from odoo.addons.l10n_cl_edi.tests.common import TestL10nClEdiCommon


class TestL10nClEdiFixSendDteCommon(TestL10nClEdiCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tax_19 = cls.env['account.tax'].search([
            ('name', '=', '19% VAT'),
            ('type_tax_use', '=', 'sale'),
            ('company_id', '=', cls.company_data['company'].id),
        ])

    def _post_invoice(self):
        invoice = self.env['account.move'].create({
            'partner_id': self.partner_sii.id,
            'move_type': 'out_invoice',
            'invoice_date': '2019-10-23',
            'currency_id': self.env.ref('base.CLP').id,
            'journal_id': self.sale_journal.id,
            'l10n_latam_document_type_id': self.env.ref('l10n_cl.dc_a_f_dte').id,
            'invoice_line_ids': [Command.create({
                'product_id': self.product_a.id,
                'quantity': 1,
                'price_unit': 1000.0,
                'tax_ids': [Command.set(self.tax_19.ids)],
            })],
        })
        invoice.action_post()
        self.assertEqual(invoice.l10n_cl_dte_status, 'not_sent')
        return invoice

    def _trigger_cron(self, xmlid):
        with self.registry_test_mode():
            self.env.ref(xmlid).method_direct_trigger()
