# Copyright 2026 FIQ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class CodeList(models.Model):
    _name = "code.list"
    _description = "Code List"
    _order = "code, name"

    code = fields.Char(required=False, copy=False)
    name = fields.Char(required=True, copy=False, translate=True)
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    item_ids = fields.One2many(
        comodel_name="code.list.item",
        inverse_name="list_id",
        string="Items",
    )

    _sql_constraints = [
        (
            "unique_code",
            "unique(code)",
            "A code already exists",
        )
    ]

    @api.depends("code", "name")
    def _compute_display_name(self):
        for item in self:
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

    def action_open_items(self):
        self.ensure_one()
        return {
            "name": f"Items of {self.display_name}",
            "type": "ir.actions.act_window",
            "res_model": "code.list.item",
            "view_mode": "list,form",
            "domain": [("list_id", "=", self.id)],
            "context": {"default_list_id": self.id},
        }
