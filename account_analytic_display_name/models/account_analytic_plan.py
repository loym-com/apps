from odoo import api, models


class AccountAnalyticPlan(models.Model):
    _inherit = "account.analytic.plan"

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name
