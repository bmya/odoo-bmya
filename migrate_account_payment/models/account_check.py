# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    check_state = fields.Char('Estado de cheques')
