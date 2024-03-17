# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    docs_online_partner_token = fields.Char(
        string="Documentos Online Token", config_parameter='docsonline.token')
    docs_online_partner_replace_name = fields.Boolean(
        string="Replace Name", config_parameter='docsonline.replace_name')
    docs_online_partner_replace_street = fields.Boolean(
        string="Replace Address", config_parameter='docsonline.replace_street')
    docs_online_partner_replace_email = fields.Boolean(
        string="Replace Email", config_parameter='docsonline.replace_email')
