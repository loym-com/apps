from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Booking Options",
    )
