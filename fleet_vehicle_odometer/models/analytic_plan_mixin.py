from odoo import _, api, fields, models


class AnalyticPlanMixin(models.AbstractModel):
    _name = "analytic.plan.mixin"
    _description = "Analytic Plan Mixin"

    analytic_plan_id = fields.Many2one(
        comodel_name="account.analytic.plan",
        # compute="_compute_analytic_plan_id",
        inverse="_inverse_analytic_plan_id",
        related="analytic_account_id.plan_id",
        readonly=False,
        store=False,
        string="Analytic Plan",
    )
    analytic_account_id = fields.Many2one("account.analytic.account")

    @api.onchange("analytic_plan_id")
    def _onchange_analytic_plan_id(self):
        for rec in self:
            if rec.analytic_plan_id:
                rec.analytic_account_id = rec.analytic_plan_id.account_id
            else:
                rec.analytic_account_id = False

    def _inverse_analytic_plan_id(self):
        for rec in self:
            rec.analytic_plan_id = rec.analytic_plan_id or False

    @api.onchange("analytic_account_id")
    def _onchange_analytic_account_id(self):
        for rec in self:
            if rec.analytic_account_id:
                rec.analytic_plan_id = rec.analytic_account_id.plan_id
            else:
                rec.analytic_plan_id = False
