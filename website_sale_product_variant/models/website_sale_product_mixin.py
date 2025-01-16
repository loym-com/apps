from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class WebsiteSaleProductMixin(models.AbstractModel):
    _name = "website.sale.product.mixin"
    _description = 'eCommerce Product Mixin'

    # /shop IS USING THE METHODS BELOW.

    def _get_website_ribbon(self):
        return self.product_tmpl_id._get_website_ribbon()

    def _get_suitable_image_size(self, columns, x_size, y_size):
        return self.product_tmpl_id._get_suitable_image_size(columns, x_size, y_size)
    
    def _get_image_holder(self):
        self.ensure_one()
        if self.image_variant_128:
            return self
        return self.product_tmpl_id
    
    @tools.ormcache('self.id')
    def _get_first_possible_variant_id(self):
        self.ensure_one()
        return self.id

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        return self.product_tmpl_id._search_render_results(fetch_fields, mapping, icon, limit)
    
    def _get_sales_prices(self, pricelist):
        template_prices = self.product_tmpl_id._get_sales_prices(pricelist)
        variant_prices = {
            product.id: template_prices[product.product_tmpl_id.id] for product in self
        }
        return variant_prices

    def _get_suitable_image_size(self, columns, x_size, y_size):
        return self.product_tmpl_id._get_suitable_image_size(columns, x_size, y_size)
