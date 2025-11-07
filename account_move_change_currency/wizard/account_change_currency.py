import logging

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang
from markupsafe import Markup

_logger = logging.getLogger(__name__)


class AccountChangeCurrency(models.TransientModel):
    _name = 'account.change.currency'
    _description = 'Change Currency'

    currency_id = fields.Many2one(
        'res.currency',
        string='Change to',
        required=True,
        help="Select a currency to apply on the invoice",
    )
    currency_rate = fields.Float(
        'Currency Rate',
        required=True,
        digits=(16, 10),
        help="Select a currency to apply on the invoice",
    )
    inverse_currency_rate = fields.Float(
        'Inverse Currency Rate',
        digits=(16, 10),
        help="1 / Currency Rate",
    )

    def _get_move(self):
        self.ensure_one()
        move = self.env['account.move'].browse(
            self.env.context.get('active_id', False))
        if not move:
            raise ValidationError(_('No Invoice on context as "active_id"'))
        return move

    @api.onchange('currency_id')
    def _onchange_currency(self):
        move = self._get_move()
        if move.company_id.currency_id == move.currency_id:
            self.currency_rate = self.currency_id.rate
            self.inverse_currency_rate = self.currency_id.inverse_rate
        else:
            date = move.invoice_date or fields.Date.today()
            self.currency_rate = move.currency_id._convert(1.0, self.currency_id, move.company_id, date, round=False)
            if self.currency_rate != 0.0:
                self.inverse_currency_rate = 1 / self.currency_rate
            else:
                self.inverse_currency_rate = False

    @api.onchange('currency_rate')
    def _onchange_currency_rate(self):
        if self.currency_rate:
            self.inverse_currency_rate = 1 / self.currency_rate
        else:
            self.inverse_currency_rate = False

    @api.onchange('inverse_currency_rate')
    def _onchange_inverse_currency_rate(self):
        if self.inverse_currency_rate:
            self.currency_rate = 1 / self.inverse_currency_rate
        else:
            self.currency_rate = False

    def change_currency(self):
        self.ensure_one()
        move = self._get_move()
        old_amount_untaxed = move.amount_untaxed
        if self.currency_id == move.currency_id:
            return {'type': 'ir.actions.act_window_close'}
        for line in move.invoice_line_ids:
            line.price_unit = line.price_unit * self.currency_rate
            line.currency_id = self.currency_id
        if self.currency_rate >= 1:
            previous_currency = move.currency_id
            rate = self.currency_rate
        else:
            previous_currency = self.currency_id
            rate = 1 / self.currency_rate
        message = _("|| Original or Previous quotation in {0}. Rate: {1}").format(
            previous_currency.name, formatLang(self.env, rate, currency_obj=move.company_id.currency_id))
        if '||' in str(move.narration):
            move.narration = move.narration[:move.narration.find('||')] + message
        else:
            move.narration = '{0} {1}'.format(move.narration or '', message)
        body = '{message1}. {message2}: {message3}'.format(
            message1=message.split(". ")[1],
            message2=_('Original or Previous Untaxed Amount'),
            message3=formatLang(self.env, old_amount_untaxed, currency_obj=move.currency_id)
        )
        move.currency_id = self.currency_id
        body += Markup('<br />') + _('Calculated Untaxed Amount: {}').format(
            formatLang(self.env, move.amount_untaxed, currency_obj=move.currency_id))
        move.message_post(body=body)
        return {'type': 'ir.actions.act_window_close'}
