from odoo import _, api, fields, models


class AnalyticPlanMixin(models.AbstractModel):
    _name = "analytic.plan.mixin"
    _description = "Analytic Plan Mixin"

    analytic_plan_id = fields.Many2one("account.analytic.plan")
    analytic_account_id = fields.Many2one("account.analytic.account")

    @api.onchange("analytic_plan_id")
    def _onchange_analytic_plan_id(self):
        for rec in self:
            if rec.analytic_plan_id:
                return {"domain": {"analytic_account_id": [("plan_id", "=", rec.analytic_plan_id.id)]}}
            else:
                return {"domain": {"analytic_account_id": []}}
