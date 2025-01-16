import json
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale_product_variant.controllers.main import WebsiteSaleProductVariant


class WebsiteSaleFilter(object):

    def __init__(self, priority, display_type, related_field, model_name, visible_name=None, domain=[]):
        assert display_type in ("radio", "select")
        self.priority = priority
        self.display_type = display_type
        self.records = request.env[model_name]
        self.visible_name = visible_name or self.records._name
        self.domain = domain
        self.related_field = related_field
        self.selected_ids = []

        selected_ids = request.httprequest.args.get(self.records._name)
        if selected_ids:
            self.selected_ids = [int(num) for num in selected_ids.split(",") if num]


class WebsiteSaleFilterController(WebsiteSaleProductVariant):

    @http.route()
    def shop(self, page=0, category=None, brand=None, ppg=False, search="", **post):
        res = super().shop(
            page=page, category=category, search=search, brand=brand, ppg=ppg, **post
        )
        # Filters
        website = request.env['website'].get_current_website()
        website_sale_filters = website._website_sale_filters()
        website_sale_filters.sort(key=lambda f: f.priority)
        # URL arguments to keep
        keep = res.qcontext["keep"].args
        for filter in website_sale_filters:
            if filter.selected_ids:
                keep[filter.records._name] = filter.selected_ids
        # Filtered products
        domain = website.sale_product_domain()
        for filter in website_sale_filters:
            if filter.selected_ids:
                domain += [(filter.related_field, "in", filter.selected_ids)]
        products = request.env[website.shop_model].search(domain)
        # Filter options (which are relevant for the filtered products)
        for filter in website_sale_filters:
            records = getattr(products, filter.related_field)
            filter.records = request.env[records._name].search(
                filter.domain + [("id", "in", records.ids)]
            )

        res.qcontext.update(
            {
                "keep": QueryURL('/shop', **keep),
                "filters": website_sale_filters,
            }
        )
        return res
