from unittest.mock import patch

from freezegun import freeze_time

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.l10n_cl_edi.tests.common import TestL10nClEdiCommon, _check_with_xsd_patch, _is_valid_certificate


@tagged('post_install_l10n', 'post_install', '-at_install')
@patch('odoo.tools.xml_utils._check_with_xsd', _check_with_xsd_patch)
@patch('odoo.addons.certificate.models.certificate.CertificateCertificate._compute_is_valid', _is_valid_certificate)
class TestCronSendDteToSii(TestL10nClEdiCommon):
    """El cron envía al SII las facturas que quedaron en "not sent".

    Los tests no llegan al SII: en modo DEMO el envío solo marca el DTE como aceptado.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tax_19 = cls.env['account.tax'].search([
            ('name', '=', '19% VAT'),
            ('type_tax_use', '=', 'sale'),
            ('company_id', '=', cls.company_data['company'].id),
        ])
        cls.cron = cls.env.ref('l10n_cl_edi_fix_send_dte.ir_cron_send_dte_to_sii')

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

    def _run_cron(self):
        self.company_data['company'].l10n_cl_dte_service_provider = 'SIIDEMO'
        with self.registry_test_mode():
            self.cron.method_direct_trigger()

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_cron_sends_pending_invoice(self):
        invoice = self._post_invoice()
        self._run_cron()
        self.assertEqual(invoice.l10n_cl_dte_status, 'accepted')

    @freeze_time('2019-10-24T20:00:00', tz_offset=3)
    def test_failing_invoice_does_not_block_the_others(self):
        failing_invoice = self._post_invoice()
        invoice = self._post_invoice()
        AccountMove = type(self.env['account.move'])
        send_dte_to_sii = AccountMove.l10n_cl_send_dte_to_sii

        def l10n_cl_send_dte_to_sii(move, *args, **kwargs):
            if move == failing_invoice:
                raise UserError("There is not a valid certificate for the company")
            return send_dte_to_sii(move, *args, **kwargs)

        with (
            patch.object(AccountMove, 'l10n_cl_send_dte_to_sii', l10n_cl_send_dte_to_sii),
            self.assertLogs('odoo.addons.l10n_cl_edi_fix_send_dte.models.account_move', level='ERROR'),
        ):
            self._run_cron()
        self.assertEqual(failing_invoice.l10n_cl_dte_status, 'not_sent')
        self.assertEqual(invoice.l10n_cl_dte_status, 'accepted')
