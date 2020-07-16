# -*- coding: utf-8 -*-
##############################################################################
# Chilean to Argentinean Backward compatibility
# Odoo / OpenERP, Open Source Management Solution
# By Blanco Martín & Asociados - (http://blancomartin.cl).
#
# Derivative from Odoo / OpenERP / Tiny SPRL
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp import models, fields, api


class backward_compatibility(models.Model):

    _description = 'Chilean Backward compatibility'
    _inherit = 'account.invoice'

    sii_document_class_id = fields.Char(compute='_comp_sii_doc_class',string='Tipo')
    sii_document_number = fields.Char(compute='_comp_sii_doc_number',string='Folio')
    sii_service_start = fields.Date(compute='_comp_sii_svc_start',string='Inicio de Prestación')
    sii_service_end = fields.Date(compute='_comp_sii_svc_end',string='Fin de Prestación')

    # sii_caf
    # sii_caf_status
    # sii_batch_number

    @api.multi
    def _comp_sii_doc_class(self):
        for record in self:
            try:
                record.sii_document_class_id = record.afip_document_class_id.doc_code_prefix
            except:
                pass

    @api.multi
    def _comp_sii_doc_number(self):
        for record in self:
            try:
                record.sii_document_number = record.afip_document_number
            except:
                pass
    
    @api.multi
    def _comp_sii_svc_start(self):
        for record in self:
            try:
                record.sii_service_start = record.afip_service_start
            except:
                pass
    
    @api.multi
    def _comp_sii_svc_end(self):
        for record in self:
            try:
                record.sii_service_end = record.afip_service_end
            except:
                pass
