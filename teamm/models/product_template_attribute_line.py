from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template.attribute.line"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env ["teamm"]

        product = self.env["product.template"]._teamm2odoo_search()
        attribute = self.env["product.attribute"]._teamm2odoo_search()

        kwargs |= {
            "product_tmpl_id": product.id,
            "attribute_id": attribute.id,
        }

        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        attribute = self.env["product.attribute"]._teamm2odoo_search()
        kwargs["value_ids"] = attribute.value_ids.ids
        return super()._teamm2odoo_values(kwargs)
