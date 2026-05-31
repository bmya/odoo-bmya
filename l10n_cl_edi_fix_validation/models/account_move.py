from odoo import models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _l10n_cl_edi_post_validation(self):
        res = super()._l10n_cl_edi_post_validation()
        if self.l10n_cl_journal_point_of_sale_type == 'online':
            if not (self.partner_id.city or self.commercial_partner_id.city):
                raise UserError(
                    _('%(company_type)s %(partner)s has not a comune or city defined. This is mandatory for '
                      'electronic invoicing. Please edit the contact and set one.',
                    company_type=_('The company') if self.partner_id.company_type == 'company' else _('The person'),
                    partner=self.partner_id.name))
        if not self.company_id.city:
            raise UserError(_(
                'Your company has not a comune or city defined. This is mandatory for electronic '
                'invoicing. Please go to your company data, and set the correct one.'))
        return res
