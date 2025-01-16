from odoo import _, api, fields, models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    # TODO: Change base _teamm2odoo_set_record() if needed
    # @api.model
    # def _teamm2odoo_after_create(self):
    #     self.attendance_ids.unlink()
