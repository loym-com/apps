from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    resource_booking_id = fields.Many2one(
        "resource.booking",
        ondelete="cascade",
        help="A booking to show the event in the timeline."
    )

    @api.constrains("name", "date_begin", "date_end")
    def _set_a_resource_booking(self):
        Booking = self.env["resource.booking"]
        event_booking_type = self.env.ref(
            "event_sale_resource_booking_timeline.resource_booking_type_event"
        )
        for rec in self:
            if rec.product_tmpl_ids:
                duration = (rec.date_end - rec.date_begin).total_seconds() / 3600
                values = {
                    "name": rec.name,
                    "type_id": event_booking_type.id,
                    "start": rec.date_begin,
                    "duration": duration,
                }
                if rec.resource_booking_id:
                    rec.resource_booking_id.write(values)
                else:
                    rec.resource_booking_id = Booking.create(values)

    @api.ondelete(at_uninstall=False)
    def _delete_the_resource_booking(self):
        for record in self:
            record.resource_booking_id.unlink()
