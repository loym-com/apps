# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("street", "city", "zip", "country_id")
    def _is_valid_postal_address(self):
        required_keys = ["street", "city", "zip", "country_id"]
        for record in self:
            record.is_valid_postal_address = all(
                bool(getattr(record, attr)) for attr in required_keys
            )

    is_valid_postal_address = fields.Boolean(
        string="Valid postal address",
        compute="_is_valid_postal_address",
        store=True,
    )
