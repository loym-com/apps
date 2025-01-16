from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Website(models.Model):
    _inherit = "website"

    shop_model = fields.Selection(
        selection=[
            ("product.template", "Product"),
            ("product.product", "Product Variant"),
        ],
        default="product.template",
        help="Select what to see in /shop (default: Product)."
    )

    def _product2pav(self):
        """ From product model, get the relation to product attribute values"""
        self.ensure_one()
        if self.shop_model == "product.template":
            return "attribute_line_ids.value_ids"
        
        elif self.shop_model == "product.product":
            return "product_template_attribute_value_ids.product_attribute_value_id"

        raise ValidationError(
            "Website {} shop_model {} has no _product2pav().".format(
                self.name, self.shop_model
            )
        )

    def _tmpl_ids(self, search_product):
        self.ensure_one()
        if self.shop_model == "product.template":
            return search_product.ids

        elif self.shop_model == "product.product":
            return search_product.product_tmpl_id.ids

        raise ValidationError(
            "Website {} shop_model {} has no _tmpl_ids().".format(
                self.name, self.shop_model
            )
        )
