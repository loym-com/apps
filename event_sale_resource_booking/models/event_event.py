import re

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Booking Options",
    )

    @api.constrains("product_tmpl_id")
    def _create_tickets_for_product_variants(self):
        Ticket = self.env["event.event.ticket"]
        if self.product_tmpl_id:
            self.event_ticket_ids.unlink()
            for product in self.product_tmpl_id.product_variant_ids:
                # Search for an event ticket product with the current variant
                ticket = Ticket.search([
                    ("event_id", "=", self.id),
                    ("product_id", "=", product.id),
                ], limit=1)

                # If no ticket exists for this variant, create one
                if not ticket:
                    # name
                    match = re.search(r"\(([^)]*)\)", product.display_name)
                    if match:
                        name = match.group(1)
                    else:
                        name = product.display_name
                    Ticket.create(
                        {
                            "name": name,
                            "event_id": self.id,
                            "product_id": product.id,
                            "price": product.lst_price,
                        }
                    )
