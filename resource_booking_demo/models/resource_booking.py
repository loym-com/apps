from odoo import api, fields, models

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    def action_save(self):
        pass
