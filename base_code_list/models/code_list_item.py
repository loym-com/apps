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
    _sql_constraints = [
        (
            "unique_code_per_list",
            "unique(code, list_id)",
            "A code of the same list already exists",
        )
    ]
    _rec_name = "display_name"

    @api.depends("code", "name", "list_id.code", "list_id.name")
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"{r.list_id.code or r.list_id.name}: {r.code or ''} {r.name}"

    display_name = fields.Char(
        compute="_compute_display_name",
        store=True,
    )
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
