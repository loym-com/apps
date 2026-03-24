from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_self_service = fields.Boolean(
        string="Is Self Service",
    )
    self_service_step = fields.Selection(
        selection=[
            ('0.1', '0.1'),
            ('1', '1'),
            ('10', '10'),
            ('100', '100'),
            ('1000', '1000'),
        ],
        string="Self Service Step",
        default="1",
    )
