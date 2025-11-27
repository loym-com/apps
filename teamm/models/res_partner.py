from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

GENDER = {
    "F": "female",
    "M": "male",
}


class ResPartner(models.Model):
    _inherit = "res.partner"

    teamm_contact_id = fields.Char("TeamM Contact ID", index=True, copy=False)

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        teamm_contact_id = self._teamm2odoo_get_value("teamm_contact_id")
        if teamm_contact_id:
            kwargs |= {"teamm_contact_id": teamm_contact_id}
        else:
            # Without teamm_contact_id, don't return any contact.
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
                "teamm_contact_id": self._teamm2odoo_get_value("teamm_contact_id"),
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
