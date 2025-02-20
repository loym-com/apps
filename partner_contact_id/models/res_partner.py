# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    person_id = fields.Char("Person ID")
