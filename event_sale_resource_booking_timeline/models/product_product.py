from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_resource_booking(self):
        action = super().action_view_resource_booking()
        # Bookings to show:
        # 1. Bookings of this product
        # Timeline view must also show these bookings:
        # 2. Combinations related to this product
        # 3. Events
        combination_ids = self._get_resource_booking_combination_ids()
        event_booking_type = self.env.ref(
            "event_sale_resource_booking_timeline.resource_booking_type_event"
        )
        action["domain"] = [
            "|",
            "|",
            ("product_id", "=", self.id),
            ("combination_id", "in", combination_ids),
            ("type_id", "=", self.env.ref(event_booking_type).id),
        ]
        return action

    def _get_resource_booking_combination_ids(self):
        self.ensure_one()
        return (
            self.resource_booking_type_combination_rel_id.combination_id.id
            or
            self.resource_booking_type_id.combination_rel_ids.mapped(
                "combination_id"
            ).ids
        )
