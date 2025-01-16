from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class EventEvent(models.Model):
    _inherit = "event.event"
    
    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env ["teamm"]
        kwargs = super()._teamm2odoo_search_kwargs(kwargs)

        create_event = self.env.context["teamm_params"].get("create_event", "0")
        if int(create_event):
            kwargs |= {
                "date_begin": TeamM._get_datetime("from"),
                "date_end": TeamM._get_datetime("to"),
            }

        return kwargs

    @api.model
    def _teamm2odoo_values(self, kwargs):
        # Multiple products names, therefore .search() instead of ._teamm2odoo_search()
        product_names = self.env["product.template"]._teamm2odoo_names()
        products = self.env["product.template"].search([("name", "in", product_names)])
        kwargs |= {
            "resource_booking_id": self.env["resource.booking"]._teamm2odoo_search().id,
            "product_tmpl_ids": products.ids,
        }
        odoo_values = super()._teamm2odoo_values(kwargs)

        # # TODO: Create event ticket
        # odoo_values |= {
        #     "event_ticket_ids": [
        #         fields.Command.create(
        #             {
        #                 "product_id": self.env["product.product"].search(
        #                     [("name", "=", "EVENT PRODUCT")]
        #                 ).id,
        #             }
        #         )
        #     ],
        # }
        return odoo_values

    @api.model
    def _teamm2odoo_get_value(self, key):
        # FIXME: Hard-coded for Fredheim
        if key == "event.event":
            try:
                year = self.env["teamm"]._get_date("from").year
                if year == 2024:
                    value = super()._teamm2odoo_get_value(key)
                    return f"2024-{value}"
                elif year < 2024:
                    return f"{year}"
            except AssertionError:
                pass

        return super()._teamm2odoo_get_value(key)
