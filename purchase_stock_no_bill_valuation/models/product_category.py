from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    reevaluate_on_bill_price_difference = fields.Boolean(company_dependent=True,
        help="Reevaluate products when there is a price difference between the Purchase Order and the Vendor Bill")
