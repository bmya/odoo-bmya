from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_cl_customs_transport_type = fields.Selection(
        [('01', '01. River, Lake or Maritime'),
         ('04', '04. Air Transport'),
         ('05', '05. Postal Transport'),
         ('06', '06. Railway'),
         ('07', '07. Highway / by land'),
         ('08', '08. Pipeline'),
         ('09', '09. Electrical wiring (overhead or underground power lines'),
         ('10', '10. Other')],  string='Company Seller Identification')
    l10n_cl_customs_packages_types = fields.Many2one('l10n_cl.customs.packages.types', string='Customs Package Types')
    l10n_cl_customs_ports = fields.Many2one('l10n_cl.customs.ports', string='Customs Ports')
