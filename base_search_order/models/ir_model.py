from odoo import models, fields


class IrModel(models.Model):
    _inherit = "ir.model"

    order_custom = fields.Char(
        "Custom Order",
        help="Custom order for the model.\nRESTART after changing this field.",
    )
