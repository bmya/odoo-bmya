import logging
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tests import Form

_logger = logging.getLogger(__name__)


class AccountChangeCurrency(models.TransientModel):
    _name = 'account.change.currency'
    _description = 'Change Currency'

    currency_id = fields.Many2one(
        'res.currency',
        string='Change to',
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
        help="Select a currency to apply on the invoice"
    )
    currency_rate = fields.Float(
        'Currency Rate',
        required=True,
        help="Select a currency to apply on the invoice"
    )
    inverse_currency_rate = fields.Float(
        'Inverse Currency Rate',
    )
    currency_rate_readonly = fields.Float(
        related='currency_rate',
        readonly=True,
        digits=lambda self: self.env['decimal.precision'].precision_get('Currency')
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

    def change_currency(self):
        self.ensure_one()
        move = self._get_move()

        with Form(move) as move_form:
            for i in range(len(move_form.invoice_line_ids)):
                with move_form.invoice_line_ids.edit(i) as line:
                    line.price_unit = line.price_unit * self.currency_rate
                    line.currency_id = self.currency_id
                if self.currency_rate >= 1:
                    message = _("|| Original quotation in {0}. Rate: {1} {2} per {0}.").format(
                        move.currency_id.name, self.currency_id.name, round(self.currency_rate, 4))
                else:
                    message = _("|| Original quotation in {0}. Rate: {0} {2} per {1}.").format(
                        move.currency_id.name, self.currency_id.name, round(self.inverse_currency_rate, 4))
            if '||' in move_form.narration:
                move_form.narration = move_form.narration[:move_form.narration.find('||')] + message
            else:
                move_form.narration = '%s %s' % (move_form.narration, message)
            move_form.currency_id = self.currency_id
            move_form.save()

        move.message_post_with_view(
            'account_move_change_currency.message_currency_rate', values={
                'message': message[3:]}, subtype_id=self.env.ref('mail.mt_note').id)
        return {'type': 'ir.actions.act_window_close'}
