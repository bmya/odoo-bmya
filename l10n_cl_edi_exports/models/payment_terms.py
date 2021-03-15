from odoo import _, api, fields, models


class PaymentTerms(models.Model):
    _inherit = "account.payment.term"

    l10n_cl_sale_modality = fields.Selection(
        [('1', '1. Assert'), ('2', '2. Under Condition'), ('3', '3. On consignment - Open'),
         ('4', '4. On consignment with minimum assert'), ('5', '5. Without payment')],  string='Sale Mode')
    l10n_cl_customs_payment_terms = fields.Many2one('l10n_cl.customs.payment.terms', string='Customs Payment Term')
