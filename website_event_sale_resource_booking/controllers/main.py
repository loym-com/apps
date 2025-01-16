import json

from datetime import datetime

from odoo import http
from odoo.http import request

    
class EventRegistration(http.Controller):

    @http.route('/event/get_available_combinations', type='http', auth='public')
    def get_combinations(self, event_id, product_id):
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
