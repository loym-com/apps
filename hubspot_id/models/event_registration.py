from odoo import api, fields, models

class EventRegistration(models.Model):
    _inherit = "event.registration"

    hubspot_deal_id = fields.Char()

    _sql_constraints = [
        (
            "hubspot_unique",
            "unique (hubspot_deal_id)",
            "Hubspot Deal ID must be unique!",
        )
    ]
