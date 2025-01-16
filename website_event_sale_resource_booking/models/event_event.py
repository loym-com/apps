from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    def get_available_products(self):
        self.ensure_one()
        records = self.env["website.event.booking.combination"].search(
            [
                ("event_id", "=", self.id),
                ("available", "=", True),
            ]
        )
        products = {record.product_id for record in records}
        products = sorted(products, key=lambda p: p.resource_booking_type_id.name)
        return products
