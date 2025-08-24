import json

from datetime import datetime

from odoo import http
from odoo.http import request

# from collections import defaultdict
# from odoo.http import request, route

from odoo.addons.website_sale_resource_booking.controllers import main as wsrb_main
from odoo.addons.website_event_sale.controllers import main as wes_main


class WebsiteSale(wsrb_main.WebsiteSale):

    def checkout_redirection(self, order):

        """Redirect to scheduling bookings if still not done."""
        order.order_line._sync_resource_bookings()
        bookings = order.mapped("order_line.resource_booking_ids")
        for booking in bookings:
            if booking.state == "pending":
                return request.redirect("/shop/booking/1/schedule")
        return super().checkout_redirection(order)


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
