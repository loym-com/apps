from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    event_registration_id = fields.Many2one("event.registration")

    def _update_attendee_and_booking(self):
        """
        Online event registration will create records in this order:
        1. sale.order
        2. sale.order.line
        3. resource.booking
        4. event.registration (will trigger this method)
        """
        for line in self:
            if line.event_registration_id and line.resource_booking_id:
                attendee = line.event_registration_id
                booking = line.resource_booking_id
                # Update attendee
                attendee.resource_booking_id = booking.id
                # Update booking
                booking.name = ", ".join([p.name for p in booking.partner_ids])
                booking.start = attendee.event_id.date_begin
                booking.stop = attendee.event_id.date_end
                booking.state = "scheduled"
        return True
