from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

GENDER = {
    "F": "female",
    "M": "male",
}


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        ref = self._teamm2odoo_get_value("ref")
        if ref:
            kwargs |= {"ref": ref}
        else:
            # Without ref, don't return any contact.
            kwargs |= {"id": 0}
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        TeamM = self.env["teamm"]
        Country = self.env["res.country"]
        PartnerCategory = self.env["res.partner.category"]

        country_code = self._teamm2odoo_get_value("country")
        if country_code == "Norge":
            country_code = "NO"
        country = Country.search([("code", "=", country_code)])

        categories = PartnerCategory
        category_names = self._teamm2odoo_get_value("customer category")
        for name in category_names:
            categories |= PartnerCategory.search([("name", "=", name)])

        url = self.env.context["teamm"].url
        if url and url[-12:] == "/orders/list":
            odoo_values = {
                # "firstname": values["mainGuest"]["firstName"],
                # "lastname": values["mainGuest"]["lastName"],
            }
        else:
            kwargs |= {
                "ref": self._teamm2odoo_get_value("ref"),
                "firstname": self._teamm2odoo_get_value("firstname"),
                "lastname": self._teamm2odoo_get_value("lastname"),
                "email": self._teamm2odoo_get_value("email"),
                "mobile": self._teamm2odoo_get_value("phone"),
                "street": self._teamm2odoo_get_value("street"),
                "zip": self._teamm2odoo_get_value("zip"),
                "city": self._teamm2odoo_get_value("city"),
                "country_id": country.id,
                "category_id": categories.ids,
                "birthdate_date": TeamM._get_date("birth date"),
                "gender": GENDER.get(self._teamm2odoo_get_value("gender")),
            }
        return super()._teamm2odoo_values(kwargs)
