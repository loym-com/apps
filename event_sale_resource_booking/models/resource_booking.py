import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    event_registration_id = fields.Many2one(
        "event.registration",
        ondelete="cascade",
    )
    event_id = fields.Many2one(
        "event.event",
        related="event_registration_id.event_id",
    )

    def _get_available_slots(self, start_dt, end_dt):
        result = super()._get_available_slots(start_dt, end_dt)
        # If the product has booking events,
        # then restrict to these events.
        # dt = datetime
        # dts = list of datetimes
        booking_events = self.product_id.event_ids
        if booking_events:
            new_result = defaultdict(list)
            for result_date, result_dts in result.items():
                new_dts = []
                for result_dt in result_dts:
                    start = result_dt.astimezone(pytz.utc).replace(tzinfo=None)
                    stop = start + timedelta(hours=self.duration)
                    for event in booking_events:
                        if (
                            event.date_begin <= start < event.date_end
                            and
                            event.date_begin < stop <= event.date_end
                        ):
                            new_result[result_date].append(result_dt)
            result = new_result
        return result
