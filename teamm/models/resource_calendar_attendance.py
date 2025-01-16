from odoo import _, api, fields, models


class ResourceCalendarAttendance(models.Model):
    _inherit = "resource.calendar.attendance"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        Calendar = self.env["resource.calendar"]
        kwargs |= {
            "calendar_id": Calendar._teamm2odoo_search().id,
            "dayofweek": self._teamm2odoo_get_value("day of week"),
            "day_period": self._teamm2odoo_get_value("day period"),
        }
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        odoo_values = super()._teamm2odoo_values(kwargs)
        odoo_values |= {
            "name": self._teamm2odoo_name(),
            "hour_from": self._teamm2odoo_get_value("hour from"),
            "hour_to": self._teamm2odoo_get_value("hour to"),
        }
        return odoo_values
