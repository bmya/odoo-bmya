import logging

from docutils.nodes import classifier

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tests import Form
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
            self._context.get('active_id', False))
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
        if self.currency_id == move.currency_id:
            return {'type': 'ir.actions.act_window_close'}
        if self.currency_id == move.company_id.currency_id:
            rate = self.currency_rate
        else:
            rate = 1 / self.currency_rate
        with Form(move) as move_form:
            for i in range(len(move_form.invoice_line_ids)):
                with move_form.invoice_line_ids.edit(i) as line:
                    line.price_unit = line.price_unit * rate
                    line.currency_id = self.currency_id
            if self.currency_rate >= 1:
                previous_currency = move.currency_id
            else:
                previous_currency = self.currency_id
            message = _("|| Original quotation in {0}. Rate: {1}").format(
                previous_currency.name, formatLang(self.env, self.currency_rate, currency_obj=move.company_id.currency_id))
            if '||' in str(move_form.narration):
                move_form.narration = move_form.narration[:move_form.narration.find('||')] + message
            else:
                move_form.narration = '%s %s' % (move_form.narration or '', message)
            body = _('%s. Original Untaxed Amount: %s. ', message.split(". ")[1], formatLang(self.env, move.amount_untaxed, currency_obj=move.currency_id))
            move_form.currency_id = self.currency_id
            move_form.save()
        body += Markup('<br />') + _('Calculated Untaxed Amount: %s', formatLang(self.env, move.amount_untaxed, currency_obj=move.currency_id))
        move.message_post(body=body, body_is_html=True)
        return {'type': 'ir.actions.act_window_close'}
