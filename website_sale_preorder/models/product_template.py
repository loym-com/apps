from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _sql_constraints = [
        ('unique_external_url',
         'unique(external_url)',
         'The External URL must be unique!'),
    ]

    @api.model
    def _get_default_usd_currency(self):
        usd_currency = self.env.ref("base.USD")
        return usd_currency.id

    external_name = fields.Char(
        string="External Name",
    )
    external_url = fields.Char(
        string="External URL",
        index=True,
    )
    external_currency_id = fields.Many2one(
        "res.currency",
        string="External Currency",
        default=_get_default_usd_currency,
    )
    external_price = fields.Monetary(
        string="Price (USD)",
        currency_field="external_currency_id",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            name = vals.get("external_name")
            url = vals.get("external_url")
            price = vals.get("external_price")
            if name and url and price:
                vals["name"] = name
                vals["website_published"] = True
                vals["website_id"] = 56
                vals["public_categ_ids"] = [Command.set([45])]
                vals["company_id"] = 15
                vals["description_sale"] = vals["external_url"]

                if url.startswith("https://remnantpublications.com/"):
                    vals["list_price"] = price * 14
                    vals["categ_id"] = 84

                elif url.startswith("https://safeliz.com/"):
                    vals["list_price"] = price * 14
                    vals["categ_id"] = 129

                else:
                    raise UserError("Url should start with https://remnantpublications.com/ or https://safeliz.com/")

        return super().create(vals_list)
