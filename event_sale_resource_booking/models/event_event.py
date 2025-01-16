from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        relation="product_template_event_rel",
        string="Booking Options",
    )
