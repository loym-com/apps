import json

from datetime import datetime

from odoo import http
from odoo.http import request

# from collections import defaultdict
# from odoo.http import request, route

from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController

    
class EventRegistration(http.Controller):

    @http.route('/event/get_available_combinations', type='http', auth='public')
    def get_available_combinations(self, event_id, product_id):
        combinations = request.env["website.event.booking.combination"].search(
            [
                ("event_id", "=", int(event_id)),
                ('product_id', '=', int(product_id)),
                ("available", "=", True),
            ]
        )
        combi_list = [
            {'id': comb.combination_id.id, 'name': comb.combination_id.name}
            for comb in combinations
        ]
        return json.dumps(combi_list)


class WebsiteEventSaleResourceBookingController(WebsiteEventSaleController):

    def _create_attendees_from_registration_post(self, event, registration_data):
        # we have at least one registration linked to a ticket -> sale mode activate
        if not any(info.get('event_ticket_id') for info in registration_data):
            return super()._create_attendees_from_registration_post(event, registration_data)

        event_ticket_ids = [registration['event_ticket_id'] for registration in registration_data if registration.get('event_ticket_id')]
        event_ticket_by_id = {
            event_ticket.id: event_ticket
            for event_ticket in request.env['event.event.ticket'].sudo().browse(event_ticket_ids)
        }

        for data in registration_data:
            ticket_id = data.get("event_ticket_id")
            if ticket_id:
                ticket = request.env["event.event.ticket"].browse(ticket_id)
                product = ticket.product_id
                booking_type = product.resource_booking_type_id
                if booking_type:
                    partner = request.env.user.partner_id
                    values = {
                        "name": partner.name,
                        # "combination_auto_assign": 0,
                        # "combination_id": combination.id,
                        "product_id": product.id,
                        "partner_ids": partner.ids,
                        "type_id": booking_type.id,
                        "start": event.date_begin,
                        "duration": (event.date_end - event.date_begin).total_seconds() / 3600,
                    }
                    booking = request.env["resource.booking"].create(values)
                    data["resource_booking_id"] = booking.id

        return super()._create_attendees_from_registration_post(event, registration_data)
