from dateutil.relativedelta import relativedelta

from odoo import fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    state = fields.Selection(inverse="_inverse_state")

    def _inverse_state(self):
        for record in self:
            record.state = record.state
