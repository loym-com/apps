# Copyright 2026 FIQ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class CodeListMixin(models.AbstractModel):
    _name = "code.list.mixin"
    _description = "Code List Mixin"

    code_list_usage_ids = fields.One2many(
        comodel_name="code.list.usage",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        copy=True,
    )
    code_list_item_ids = fields.Many2many(
        comodel_name="code.list.item",
        compute="_compute_code_list_item_ids",
        string="Code List Items",
        search="_search_code_list_item_ids",
    )

    @api.depends("code_list_usage_ids.code_list_item_id")
    def _compute_code_list_item_ids(self):
        for record in self:
            record.code_list_item_ids = record.code_list_usage_ids.mapped(
                "code_list_item_id"
            )

    @api.model
    def _search_code_list_item_ids(self, operator, value):
        if operator not in ("=", "!=", "ilike", "not ilike", "=ilike", "=like", "like", "not like", "=not like"):
            return []

        # Search for code_list_usage_ids that match the criteria
        usage_ids = self.env["code.list.usage"].search([
            ("code_list_item_id", operator, value),
            ("model", "=", self._name),
        ]).mapped("res_id")

        # Return domain to filter records based on the search
        return [("id", "in", usage_ids)]
