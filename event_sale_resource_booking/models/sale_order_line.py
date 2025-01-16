from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    event_registration_id = fields.Many2one("event.registration")
