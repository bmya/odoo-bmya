import logging

from docutils.nodes import classifier

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tools.misc import formatLang

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
        if self.currency_id in move.currency_id:
            return {'type': 'ir.actions.act_window_close'}
        fa_arrow = ('<i class="o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600" title="Changed" '
                    'role="img" aria-label="Changed"/>')
        class_new_value = 'class="o_TrackingValue_newValue me-1 fw-bold text-info"'
        class_old_value = 'class="o_TrackingValue_oldValue me-1 px-1 text-muted fw-bold"'
        with Form(move) as move_form:
            for i in range(len(move_form.invoice_line_ids)):
                with move_form.invoice_line_ids.edit(i) as line:
                    line.price_unit = line.price_unit * self.currency_rate
                    line.currency_id = self.currency_id
            if self.currency_rate >= 1:
                message = _("|| Quotation previously in {0}. Rate: {1} {2} per {0}.").format(
                    move.currency_id.name, self.currency_id.name, round(self.currency_rate, 4))
            else:
                message = _("|| Quotation previously in {0}. Rate: {0} {2} per {1}.").format(
                    move.currency_id.name, self.currency_id.name, round(self.inverse_currency_rate, 4))
            if '||' in str(move_form.narration):
                move_form.narration = move_form.narration[:move_form.narration.find('||')] + message
            else:
                move_form.narration = '%s %s' % (move_form.narration or '', message)
            str_curr = _("Currency")
            str_untaxed = _("Untaxed amount")
            body = (f'<div {class_old_value}>{_(message.split(". ")[1])}<br/>'
                    f'{str_curr}: {move.currency_id.name} {fa_arrow} <span {class_new_value}>'
                    f'{self.currency_id.name}</span><br/>'
                    f'{str_untaxed}: {formatLang(self.env, move.amount_untaxed, currency_obj=move.currency_id)} '
                    f'{fa_arrow} ')
            move_form.currency_id = self.currency_id
            move_form.save()
        body += (f'<span {class_new_value}>{formatLang(self.env, move.amount_untaxed, currency_obj=move.currency_id)}'
                 '</span></div>')
        move.message_post(body=body)
        return {'type': 'ir.actions.act_window_close'}
