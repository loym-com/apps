from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    event_ids = fields.Many2many(
        comodel_name="event.event",
        relation="product_template_event_rel",
        string="Events with booking",
    )
