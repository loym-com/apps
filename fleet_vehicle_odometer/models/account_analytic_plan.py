from odoo import _, api, fields, models


class AccountAnalyticPlan(models.AbstractModel):
    _inherit = "account.analytic.plan"

    active = fields.Boolean(default=True)
