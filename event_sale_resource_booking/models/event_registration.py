from odoo import api, fields, models
from odoo.exceptions import UserError


class EventRegistration(models.Model):
    _inherit = "event.registration"

    resource_booking_id = fields.Many2one(
        "resource.booking",
        string="Booking",
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        "product.product",
        readonly=False,
        help="Online registration: Select product"
    )
    resource_booking_combination_id = fields.Many2one(
        "resource.booking.combination",
        readonly=False,
        string="Booked",
        help="Online registration: Select combination"
    )

    """ SET RESOURCE BOOKING """

    @api.model
    def create(self, vals_list):
        attendees = super().create(vals_list)
        attendees._update_sale_order_line()
        attendees.mapped('sale_order_line_id')._update_attendee_and_booking()
        return attendees

    def _update_sale_order_line(self):
        for attendee in self:
            order_line = attendee.sale_order_line_id
            if order_line:
                # Link attendee to order line
                order_line.event_registration_id = attendee.id
                # Link booking to order line
                bookings = order_line.resource_booking_ids
                if bookings and len(bookings) == 1:
                    # This is also done here:
                    # https://github.com/norlinhenrik/oca-sale-workflow/blob/16.0-imp-sale_resource_booking-fredheim/sale_resource_booking/models/sale_order_line.py#L97
                    order_line.resource_booking_id = bookings.id
