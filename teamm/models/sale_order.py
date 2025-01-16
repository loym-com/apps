from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _teamm2odoo_values(self, kwargs):
        TeamM = self.env["teamm"]
        main_guest = self._teamm2odoo_get_value("main guest")

        # FIXME: Hard-coded for Fredheim
        if TeamM._get_date("from").year < 2024:
            main_guest = True

        if main_guest in ("Yes", "SANN", "TRUE", True, 1):
            kwargs |= {
                "partner_id": self.env["res.partner"]._teamm2odoo_search().id,
                "date_order": TeamM._get_date("booked at"),
                "state": "sale",
            }

            # FIXME: Hard-coded for Fredheim
            start_date = TeamM._get_date("from")
            if start_date.year < 2024:
                kwargs["invoice_status"] = ""

            return super()._teamm2odoo_values(kwargs)

    @api.model
    def _teamm2odoo_name(self):
        name = super()._teamm2odoo_name()
        if name[:1] == "T":
            name = name[1:]
        name = f"T{name.zfill(5)}"
        return name
