from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = "product.product"
    _inherit = [
        "product.product",
        "website.searchable.mixin",
        "website.sale.product.mixin",
    ]
