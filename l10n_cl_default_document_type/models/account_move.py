from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_l10n_latam_document_type(self):
        for r in self:
            doc_types = r.l10n_latam_available_document_type_ids._origin
            invoice_type = r.move_type
            if invoice_type in ['out_refund', 'in_refund']:
                doc_types = doc_types.filtered(lambda x: x.internal_type not in ['debit_note', 'invoice'])
            elif invoice_type in ['out_invoice', 'in_invoice']:
                doc_types = doc_types.filtered(lambda x: x.internal_type not in ['credit_note'])
            if r.debit_origin_id:
                doc_types = doc_types.filtered(lambda x: x.internal_type == 'debit_note')

            partner_type = self.partner_id.l10n_cl_sii_taxpayer_type
            if partner_type in ['1', '2']:
                r.l10n_latam_document_type_id = doc_types and doc_types.filtered_domain([('code', '=', '33')]).id
            elif partner_type == '3':
                r.l10n_latam_document_type_id = doc_types and doc_types.filtered_domain([('code', '=', '39')]).id
            elif partner_type == '4':
                r.l10n_latam_document_type_id = doc_types and doc_types.filtered_domain([('code', '=', '110')]).id
            else:
                r.l10n_latam_document_type_id = doc_types and doc_types[0].id
