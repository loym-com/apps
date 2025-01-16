from odoo import _, fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    def sale_product_domain(self):
        domain = super(Website, self).sale_product_domain()
        if self.shop_model == "website.event.booking.combination":
            filters = self._website_sale_filters()
            for f in filters:
                if f.selected_ids:
                    domain += [(f.related_field, "in", f.selected_ids)]
        return domain

    def _website_sale_filters(self):
        return []
