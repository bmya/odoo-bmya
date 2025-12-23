from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'


    def _compute_l10n_latam_document_type(self):
        # Separate records that should use Chilean taxpayer logic
        cl_moves_with_taxpayer = self.filtered(
            lambda m: m.partner_id.l10n_cl_sii_taxpayer_type and
                     m.l10n_latam_available_document_type_ids
        )

        for r in cl_moves_with_taxpayer:
            invoice_type = r.move_type
            doc_types_dict = {
                doc_type.code: doc_type for doc_type in r.l10n_latam_available_document_type_ids._origin
            }
            taxpayer_type = r.partner_id.l10n_cl_sii_taxpayer_type

            if taxpayer_type in ['1', '2']:
                code = '46' if invoice_type == 'in_invoice' else '33'  # 46=Factura Compra, 33=Factura Venta
                r.l10n_latam_document_type_id = doc_types_dict.get(code, False)
            elif taxpayer_type == '3':
                r.l10n_latam_document_type_id = doc_types_dict.get('39', False)
            elif taxpayer_type == '4':
                r.l10n_latam_document_type_id = doc_types_dict.get('110', False)

        # For other records, use standard Odoo behavior
        other_moves = self - cl_moves_with_taxpayer
        if other_moves:
            super(AccountMove, other_moves)._compute_l10n_latam_document_type()
