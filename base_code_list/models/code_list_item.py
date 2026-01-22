# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# Copyright 2026 FIQ
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


# There are so many code lists that can be useful in Odoo
# that it would be stupid to have one object for each UNCL
# because it would duplicate the python code, views, menu entries, ACL, etc...
# So I decided to have a single object with a type field
class CodeListItem(models.Model):
    _name = "code.list.item"
    _description = "Code List Item"
    _order = "list_id, code, name"

    code = fields.Char(required=False, copy=False)
    name = fields.Char(required=True, copy=False, translate=True)
    description = fields.Text(translate=True)
    list_id = fields.Many2one(
        "code.list",
        string="Code List",
        required=True,
        ondelete="restrict",
    )
    parent_id = fields.Many2one(
        "code.list.item",
        string="Parent Item",
        ondelete="restrict",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "unique_code_per_list",
            "unique(code, list_id)",
            "A code of the same list already exists",
        )
    ]

    @api.depends("code", "name")
    @api.depends_context("include_list_code")
    def _compute_display_name(self):
        include_list_code = self.env.context.get("include_list_code")
        for item in self:
            if include_list_code:
                item.display_name = f"{item.list_id.code or item.list_id.name}: {item.code or ''} {item.name}"
            else:
                item.display_name = f"{item.code or ''} {item.name}"

    # _rec_names_search = ['name', 'code'] doesn't give the result we want
    # We want that, when you type an exact code, you get only that code
    # Exemple : on UNECE Tax category, when you type "S", you should get only
    # "[S] Standard rate"
    @api.model
    def _search_display_name(self, operator, value):
        if value and operator == "ilike":
            ids = list(self._search([("code", "=", value)]))
            if ids:
                return [("id", "in", ids)]
        return super()._search_display_name(operator, value)
