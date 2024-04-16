from odoo import _, api, fields, models


class MisBudgetByAccountItem(models.Model):
    _inherit = "mis.budget.by.account.item"

    account_tag_ids = fields.Many2many(
        "account.account.tag",
        related="account_id.tag_ids",
    )
