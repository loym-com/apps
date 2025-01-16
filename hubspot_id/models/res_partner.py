from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"


    hubspot_contact_id = fields.Char()

    _sql_constraints = [
        (
            "hubspot_unique",
            "unique (hubspot_contact_id)",
            "Hubspot Contact ID must be unique!",
        )
    ]
