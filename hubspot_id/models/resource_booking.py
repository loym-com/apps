from odoo import api, fields, models

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    hubspot_deal_id = fields.Char()

    _sql_constraints = [
        (
            "hubspot_unique",
            "unique (hubspot_deal_id)",
            "Hubspot Deal ID must be unique!",
        )
    ]
