from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_cl_block_self_invoice = fields.Boolean(
        string="Block self-invoicing",
        config_parameter='l10n_cl_edi_fix_validation.block_self_invoice',
        default=True,
        help="Prevent issuing an electronic document where the issuer and receiver have the same RUT.")
    l10n_cl_block_period_closed = fields.Boolean(
        string="Block documents from a closed SII period",
        config_parameter='l10n_cl_edi_fix_validation.block_period_closed',
        default=True,
        help="Prevent issuing electronic documents dated in a month already closed at the SII, "
             "even if the accounting period itself is not locked.")
    l10n_cl_period_closing_day = fields.Integer(
        string="SII period closing day",
        config_parameter='l10n_cl_edi_fix_validation.period_closing_day',
        default=20,
        help="Day of the month on which the SII closes the previous month's tax period.")
