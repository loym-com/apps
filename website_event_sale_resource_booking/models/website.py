from datetime import datetime

from odoo.http import request

from odoo import _, fields, models

from odoo.addons.website_sale_filter.controllers.main import WebsiteSaleFilter


class Website(models.Model):
    _inherit = "website"

    shop_model = fields.Selection(
        selection_add=[("website.event.booking.combination", "Event Booking Variant")]
    )

    def _product2pav(self):
        """ From product model, get the relation to product attribute values"""        
        if self.shop_model == "website.event.booking.combination":
            return "product_template_attribute_value_ids.product_attribute_value_id"
        return super()._product2pav()

    def _tmpl_ids(self, search_product):
        if self.shop_model == "website.event.booking.combination":
            return search_product.product_tmpl_id.ids
        return super()._tmpl_ids(search_product)
    
    def _website_sale_filters(self):
        filters = super()._website_sale_filters()
        add = [
            (30, "select", "event_id", "event.event", _("Event"), [("date_end", ">", datetime.now())]),
            (40, "select", "resource_booking_type_id", "resource.booking.type", _("Booking Type")),
            (50, "select", "combination_id", "resource.booking.combination", _("Booking")),
            (60, "radio", "resource_group_tag_ids", "resource.group.tag", _("Tags")),
        ]
        for values in add:
            filters.append(WebsiteSaleFilter(*values))
        return filters
