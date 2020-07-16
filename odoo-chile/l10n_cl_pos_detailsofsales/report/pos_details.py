from openerp import api, models
from openerp.addons.point_of_sale.report.pos_details import pos_details

class report_parser(pos_details):
    
    def _get_invoice1(self, inv_id):
        res = {}
        if inv_id:
            self.cr.execute(
                """select 
concat(sc.doc_code_prefix,ai.sii_document_number)
from 
account_invoice as ai 
join sii_document_class as sc
on ai.sii_document_class_id = sc.id
where ai.id = %s""",
                (inv_id,))
            res = self.cr.fetchone()
            return res[0] or 'Draft'
        else:
            return ''

    def __init__(self, cr, uid, name, context):
        super(report_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'getinvoice': self._get_invoice1,
        })
        
    # def set_context(self, objects, data, ids, report_type=None):
    #     self.localcontext['data'] = data
    #     self.localcontext['objects'] = objects

    

class ReportDetails(models.AbstractModel):
    # _name = 'report.point_of_sale.report_detailsofsales'
    # _inherit = 'report.abstract_report'
    _inherit = 'report.point_of_sale.report_detailsofsales'
    _template = 'point_of_sale.report_detailsofsales'

    _wrapped_report_class = report_parser

