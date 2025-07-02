# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    docs_online_partner_url = fields.Char(
        string="DocumentosOnline URL",
        config_parameter='docsonline.url',
        default='',
        help="The base URL for the DocumentosOnline API. Leave empty to use the default provided by the system."
    )
    docs_online_partner_token = fields.Char(
        string="DocumentosOnline Token",
        config_parameter='docsonline.token',
        default=None,
        help="The authentication token for accessing the DocumentosOnline API. Keep this secure and do not share it publicly."
    )
    docs_online_partner_replace_name = fields.Boolean(
        string="Replace Partner Name",
        config_parameter='docsonline.replace_name',
        default=False,
        help="If checked, the partner's name will be overwritten with data from DocumentosOnline when updating."
    )
    docs_online_partner_replace_street = fields.Boolean(
        string="Replace Partner Address",
        config_parameter='docsonline.replace_street',
        default=False,
        help="If checked, the partner's address fields will be overwritten with data from DocumentosOnline when updating."
    )
    docs_online_partner_replace_email = fields.Boolean(
        string="Replace Partner Email",
        config_parameter='docsonline.replace_email',
        default=True,
        help="If checked, the partner's DTE email will be overwritten with data from DocumentosOnline when updating."
    )
    docs_online_partner_replace_activity = fields.Boolean(
        string="Replace Partner Activity",
        config_parameter='docsonline.replace_activity',
        default=False,
        help="If checked, the partner's activity description will be overwritten with data from DocumentosOnline when updating."
    )
    docs_online_partner_restrict_token_access = fields.Boolean(
        string="Restrict Token Access",
        config_parameter='docsonline.restrict_token_access',
        default=False,
        help="If checked, only users with specific permissions can view or modify the API token."
    )

    @api.constrains('docs_online_partner_url')
    def _check_docs_online_url(self):
        """Validate that the provided URL is well-formed."""
        for record in self:
            if record.docs_online_partner_url:
                url = record.docs_online_partner_url.strip()
                if not url.startswith(('http://', 'https://')):
                    raise ValidationError(_("DocumentosOnline URL must start with 'http://' or 'https://'."))
                if not url[8 if url.startswith('https://') else 7:]:
                    raise ValidationError(_("DocumentosOnline URL cannot be empty after the protocol."))

    @api.constrains('docs_online_partner_token')
    def _check_docs_online_token(self):
        """Validate that the token is not empty if provided."""
        for record in self:
            if record.docs_online_partner_token and not record.docs_online_partner_token.strip():
                raise ValidationError(_("DocumentosOnline Token cannot be empty or consist only of whitespace."))