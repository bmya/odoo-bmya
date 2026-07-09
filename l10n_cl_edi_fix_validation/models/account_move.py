from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import str2bool
from odoo.tools.translate import _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _l10n_cl_edi_post_validation(self):
        res = super()._l10n_cl_edi_post_validation()
        if self.l10n_cl_journal_point_of_sale_type == 'online':
            if not (self.partner_id.city or self.commercial_partner_id.city):
                raise UserError(
                    _(
                        '%(company_type)s %(partner)s has not a comune or city defined. This is mandatory for '
                        'electronic invoicing. Please edit the contact and set one.',
                        company_type=_('The company') if self.partner_id.company_type == 'company' else _('The person'),
                        partner=self.partner_id.name,
                    )
                )
        if not self.company_id.city:
            raise UserError(_(
                'Your company has not a comune or city defined. This is mandatory for electronic '
                'invoicing. Please go to your company data, and set the correct one.'))

        icp = self.env['ir.config_parameter'].sudo()
        if str2bool(icp.get_param('l10n_cl_edi_fix_validation.block_self_invoice', 'True')):
            company_vat = self.company_id.vat
            partner_vat = self.commercial_partner_id.vat
            if company_vat and partner_vat and (
                    self._l10n_cl_format_vat(company_vat) == self._l10n_cl_format_vat(partner_vat)):
                raise UserError(_(
                    'You cannot issue an electronic document to yourself. The issuer RUT '
                    '%(vat)s is the same as the receiver RUT.', vat=company_vat))

        if str2bool(icp.get_param('l10n_cl_edi_fix_validation.block_period_closed', 'True')):
            closing_day = int(icp.get_param('l10n_cl_edi_fix_validation.period_closing_day', '20'))
            today = fields.Date.context_today(self)
            months_diff = (today.year - self.invoice_date.year) * 12 + (today.month - self.invoice_date.month)
            if months_diff >= 2 or (months_diff == 1 and today.day >= closing_day):
                raise UserError(_(
                    'The tax period for %(date)s is already closed at the SII (closing day: %(day)s of '
                    'the following month). Please use the current period or adjust the invoice date.',
                    date=self.invoice_date, day=closing_day))
        return res
