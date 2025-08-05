from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    event_ids = fields.One2many(
        comodel_name="event.event",
        inverse_name="product_tmpl_id",
        string="Events with booking",
    )
