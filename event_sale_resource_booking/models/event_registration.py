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
        if type(vals_list) is dict:
            vals_list = [vals_list]
        for vals in vals_list:
            booking_vals = self._get_booking_vals(vals)
            if booking_vals:
                booking = self.env['resource.booking'].create(booking_vals)
                vals["resource_booking_id"] = booking.id
                # vals.pop("product_id")
                # vals.pop("resource_booking_combination_id")
        return super(EventRegistration, self).create(vals)

    def write(self, vals):
        for record in self:
            if vals.get("product_id") or vals.get("resource_booking_combination_id"):
                booking_vals = self._get_booking_vals(vals)
                if booking_vals:
                    booking = record.resource_booking_id
                    if booking:
                        booking.write(booking_vals)
                    else:
                        booking = self.env['resource.booking'].create(booking_vals)
                    vals["resource_booking_id"] = booking.id
                # vals.pop("product_id")
                # vals.pop("resource_booking_combination_id")
        return super().write(vals)

    def _get_booking_vals(self, vals):
        def get(field):
            if vals.get(field):
                return vals[field]
            else:
                value = getattr(self, field)
                if isinstance(value, models.Model):
                    return value.id
                else:
                    return value

        event = self.env["event.event"].browse(get("event_id"))
        if event.product_tmpl_ids and not get("resource_booking_id"):
            product_id = get("product_id")
            combination_id = get("resource_booking_combination_id")
            if not (product_id and combination_id):
                raise UserError("Missing booking product or combination.")
            product = self.env["product.product"].browse(product_id)
            booking_vals = {
                "name": get("name"),
                "partner_id": get('partner_id'), # TODO: search / create
                'type_id': product.resource_booking_type_id.id,
                'combination_id': get('resource_booking_combination_id'),
                "product_id": product.id,
                "start": event.date_begin,
                "stop": event.date_end,
            }
            return booking_vals
