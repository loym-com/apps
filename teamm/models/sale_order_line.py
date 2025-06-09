from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _teamm2odoo(self):
        # Set quantity to 0 (old booking) if no record found (new booking)
        record = self._teamm2odoo_search()
        if not record:
            lines = self.with_context(teamm_ignore_product=True)._teamm2odoo_search()
            for line in lines:
                line.write({"product_uom_qty": 0})

        records = self._teamm2odoo_set_record()

        discounts = self._teamm2odoo_get_value("discounts")
        for discount in discounts:
            self = self.with_context(teamm_discount=discount)
            records |= self._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        order = self.env["sale.order"]._teamm2odoo_search()
        booking = self.env["resource.booking"]._teamm2odoo_search()
        product = self.env["product.product"]._teamm2odoo_search()
        if not len(order) or not len(booking) or not len(product):
            hubspot_deal_id = self._teamm2odoo_get_value("hubspot deal id")
            raise ValidationError(f"Missing info for hubspot deal id {hubspot_deal_id}:\nOrder: {order}\nProduct: {product} (check discount codes)\nBooking: {booking}")
        kwargs |= {
            "order_id": order.id,
            "resource_booking_id": booking.id,
        }
        if not self.env.context.get("teamm_ignore_product"):
            kwargs |= {
                "product_id": product.id,
            }
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        TeamM = self.env ["teamm"]

        # values
        product = self.env["product.product"]._teamm2odoo_search()
        start_date = TeamM._get_date("from")
        end_date = TeamM._get_date("to")
        event = self.env["event.event"]._teamm2odoo_search()
        event_registration = self.env["event.registration"]._teamm2odoo_search()
        booking = self.env["resource.booking"]._teamm2odoo_search()
        hubspot_deal_id = self._teamm2odoo_get_value("hubspot deal id")
        if not len(product):
            debug = True
        kwargs |= {
            "name": product.display_name,
            "product_uom_qty": 1,
            "start_date": start_date,
            "end_date": end_date,
            "currency_id": self.env.company.currency_id.id,
            "event_id": event.id,
            "event_registration_id": event_registration.id,
            "hubspot_deal_id": hubspot_deal_id,
        }

        # conditional values
        discount = self.env.context.get("teamm_discount")
        if discount:
            kwargs["price_unit"] = -discount[1]
        else:
            kwargs["price_unit"] = self._teamm2odoo_get_value("subtotal")
            kwargs["resource_booking_ids"] = [(fields.Command.set([booking.id]))]
            # "resource_booking_ids" is necessary because
            # _sync_resource_bookings() needs it before the order line is saved.

        return super()._teamm2odoo_values(kwargs)

    @api.model
    def _teamm2odoo_after_create_or_write(self):
        record = self.filtered("product_id.resource_booking_type_id")
        record.resource_booking_id.sale_order_line_id = record.id
        record.resource_booking_id.sale_order_id = record.order_id.id
        record.event_registration_id.sale_order_line_id = record.id
        record.event_registration_id.sale_order_id = record.order_id.id

        # FIXME: Hard-coded for Fredheim
        if self.start_date.year < 2024:
            self.order_id.invoice_status = ""
