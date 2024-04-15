from odoo import _, api, fields, models


class AccountAccountTag(models.Model):
    _inherit = "account.account.tag"

    budget_percent = fields.Float()
