import base64

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_cl_is_vendor_doc_refund = fields.Boolean(
        string='N/C a factura de compra',
        compute='_compute_l10n_cl_is_vendor_doc_refund', store=True,
        help='Nota de crédito (61) emitida por la empresa sobre una factura de compra (46): '
             'se timbra con el CAF 61 y se envía al SII como cualquier N/C de venta.')

    @api.depends('move_type', 'company_id', 'l10n_latam_document_type_id',
                 'reversed_entry_id.l10n_latam_document_type_id',
                 'l10n_cl_reference_ids.l10n_cl_reference_doc_type_id')
    def _compute_l10n_cl_is_vendor_doc_refund(self):
        for move in self:
            move.l10n_cl_is_vendor_doc_refund = (
                move.company_id.account_fiscal_country_id.code == 'CL'
                and move.move_type == 'in_refund'
                and move.l10n_latam_document_type_id.code == '61'
                and move._l10n_cl_refunds_vendor_doc()
            )

    def _l10n_cl_refunds_vendor_doc(self):
        """ La N/C apunta a una 46, por la reversa o por una referencia cargada a mano. """
        self.ensure_one()
        return (
            self.reversed_entry_id.l10n_latam_document_type_id.code == '46'
            or '46' in self.l10n_cl_reference_ids.l10n_cl_reference_doc_type_id.mapped('code')
        )

    def _l10n_cl_partner_is_foreign(self):
        """ Mismo criterio con que l10n_cl le deja solo la 46 a un proveedor. """
        self.ensure_one()
        partner = self.partner_id
        return (partner.l10n_cl_sii_taxpayer_type not in ('1', '2', '3')
                and (partner.country_id.code != 'CL' or partner.l10n_cl_sii_taxpayer_type == '4'))

    def _l10n_cl_is_purchase_refund_with_documents(self):
        self.ensure_one()
        return (self.journal_id.company_id.account_fiscal_country_id.code == 'CL'
                and self.journal_id.type == 'purchase'
                and self.journal_id.l10n_latam_use_documents
                and self.move_type == 'in_refund')

    def _get_l10n_latam_documents_domain(self):
        self.ensure_one()
        if self._l10n_cl_is_purchase_refund_with_documents() and (
                self._l10n_cl_partner_is_foreign()
                or self.reversed_entry_id.l10n_latam_document_type_id.code == '46'):
            return [
                ('country_id.code', '=', 'CL'),
                ('internal_type', '=', 'credit_note'),
                ('code', '=', '61'),
            ]
        return super()._get_l10n_latam_documents_domain()

    def _check_document_types_post(self):
        foreign_refunds = self.filtered(
            lambda m: m._l10n_cl_is_purchase_refund_with_documents()
            and m.l10n_latam_document_type_id.code == '61'
            and m._l10n_cl_partner_is_foreign())
        for move in foreign_refunds:
            if not move._l10n_cl_refunds_vendor_doc():
                raise ValidationError(_(
                    'The credit note %s for a foreign supplier must reference the purchase invoice (46) '
                    'it cancels or corrects.', move.display_name))
        return super(AccountMove, self - foreign_refunds)._check_document_types_post()

    @api.depends('l10n_latam_document_type_id', 'journal_id', 'move_type',
                 'reversed_entry_id', 'l10n_cl_reference_ids.l10n_cl_reference_doc_type_id')
    def _compute_l10n_latam_manual_document_number(self):
        return super()._compute_l10n_latam_manual_document_number()

    def _is_manual_document_number(self):
        # En el wizard de reversa todavía no hay tipo de documento, pero sí reversed_entry_id
        if self._l10n_cl_is_purchase_refund_with_documents() and self._l10n_cl_refunds_vendor_doc():
            return False
        return super()._is_manual_document_number()

    def _get_last_sequence_domain(self, relaxed=False):
        where_string, param = super()._get_last_sequence_domain(relaxed)
        if (self.company_id.account_fiscal_country_id.code == 'CL' and self.l10n_latam_use_documents
                and self.l10n_latam_document_type_id.code == '61'):
            # El CAF 61 es uno por RUT: las N/C de venta y las N/C a una 46 comparten folios
            where_string = where_string.replace(
                'move_type IN %(move_type)s',
                "(move_type IN %(move_type)s OR (move_type = 'in_refund' AND l10n_cl_is_vendor_doc_refund))")
        return where_string, param

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        for move in res.filtered(
                lambda m: m.l10n_cl_is_vendor_doc_refund
                and m.company_id.l10n_cl_dte_service_provider in ['SII', 'SIITEST', 'SIIDEMO']
                and m.journal_id.l10n_latam_use_documents):
            move.with_context(l10n_cl_dte_rendering=True)._l10n_cl_vendor_refund_create_dte()
        return res

    def _l10n_cl_vendor_refund_create_dte(self):
        """ Lo que hace l10n_cl_edi en _post para un documento emitido, que deja fuera a esta N/C
        porque solo mira si el tipo de documento es 46. """
        self.ensure_one()
        msg_demo = _(' in DEMO mode.') if self.company_id.l10n_cl_dte_service_provider == 'SIIDEMO' else '.'
        self._l10n_cl_edi_post_validation()
        self._l10n_cl_create_dte()
        self.l10n_cl_dte_status = 'not_sent'
        dte_signed, file_name = self._l10n_cl_create_dte_envelope()
        attachment = self.env['ir.attachment'].create({
            'name': 'SII_{}'.format(file_name),
            'res_id': self.id,
            'res_model': 'account.move',
            'datas': base64.b64encode(dte_signed.encode('ISO-8859-1', 'replace')),
            'type': 'binary',
        })
        self.l10n_cl_sii_send_file = attachment.id
        self.with_context(no_new_invoice=True).message_post(
            body=_('DTE has been created%s', msg_demo),
            attachment_ids=attachment.ids)

    def _l10n_cl_get_amounts(self):
        values = super()._l10n_cl_get_amounts()
        # l10n_cl solo invierte el signo de out_invoice; en un in_refund los saldos son negativos.
        # Solo al armar el DTE: el libro de compras (l10n_cl_edi_iecv_gen) suma estos montos con
        # el signo de siempre.
        if self.env.context.get('l10n_cl_dte_rendering') and self.l10n_cl_is_vendor_doc_refund:
            for amounts in filter(None, (values, values.get('second_currency'))):
                for key in ('subtotal_amount_taxable', 'subtotal_amount_exempt', 'vat_amount'):
                    amounts[key] = -amounts[key]
        return values

    def _get_name_invoice_report(self):
        self.ensure_one()
        if self.l10n_cl_is_vendor_doc_refund and self.l10n_latam_use_documents:
            return 'l10n_cl.report_invoice_document'
        return super()._get_name_invoice_report()
