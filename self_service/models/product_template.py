from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_self_service = fields.Boolean(
        string="Is Self Service",
    )
