from odoo import _, api, fields, models


class AccountAccountTag(models.Model):
    _inherit = "account.account.tag"

    budget_input_ids = fields.One2many(
        "account.account.tag.budget.input",
        "account_tag_id",
    )
