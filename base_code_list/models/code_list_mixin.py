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
        inverse="_inverse_code_list_item_ids",
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

    def _inverse_code_list_item_ids(self):
        for record in self:
            # Get the current set of code_list_usage_ids
            existing_usages = self.env['code.list.usage'].search([
                ('model', '=', record._name),
                ('res_id', '=', record.id)
            ])

            # Determine which items to add and which to remove
            current_item_ids = record.code_list_item_ids.ids
            existing_item_ids = existing_usages.mapped('code_list_item_id').ids

            # Add new items
            items_to_add = set(current_item_ids) - set(existing_item_ids)
            for item_id in items_to_add:
                item = self.env['code.list.item'].browse(item_id)
                self.env['code.list.usage'].create({
                    'model': record._name,
                    'res_id': record.id,
                    'code_list_item_id': item.id,
                    'code_list_id': item.list_id.id,
                })

            # Remove items that are no longer in the list
            items_to_remove = set(existing_item_ids) - set(current_item_ids)
            for usage in existing_usages.filtered(lambda u: u.code_list_item_id.id in items_to_remove):
                usage.unlink()
