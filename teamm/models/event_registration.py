from datetime import datetime

from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

class EventRegistration(models.Model):
    _inherit = "event.registration"

    teamm_booking_id = fields.Char("TeamM Booking ID", index=True, copy=False)

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        teamm_booking_id = self._teamm2odoo_get_value("teamm_booking_id")
        if not teamm_booking_id:
            err_msg = "teamm_booking_id is missing: {self.env.context['teamm_values']}"
            self._teamm2odoo_raise_error(err_msg)

        kwargs |= {
            "teamm_booking_id": teamm_booking_id,
        }
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        event = self.env["event.event"]._teamm2odoo_search()
        booking = self.env["resource.booking"]._teamm2odoo_search()
        combination = self.env["resource.booking.combination"]._teamm2odoo_search()
        product = self.env["product.product"]._teamm2odoo_search()

        if not event:
            err_msg = f"Event not found for teamm_booking_id {self._teamm2odoo_get_value('teamm_booking_id')}"
            self._teamm2odoo_raise_error(err_msg)

        kwargs |= {
            "name": booking.partner_id.name,
            "email": booking.partner_id.email,
            "phone": booking.partner_id.mobile,
            "event_id": event.id,
            "resource_booking_id": booking.id,
            "resource_booking_combination_id": combination.id,
            "product_id": product.id,
            "state": "done",
        }
        return super()._teamm2odoo_values(kwargs)

    def _teamm2odoo_after_create_or_write(self):
        booking = self.env["resource.booking"]._teamm2odoo_search()
        booking.event_registration_id = self.id
