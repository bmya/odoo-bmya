from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cl_company_xml_identification = fields.Char('Company Seller Identification', help='CdgVendedor')
    l10n_cl_partner_xml_identification = fields.Char('Customer Identification', help='CdgIntRecep')
