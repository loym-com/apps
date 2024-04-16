from odoo import _, api, fields, models


class AccountAccountTag(models.Model):
    _inherit = "account.account.tag"

    budget_kpi_old = fields.Float()
    budget_kpi_new = fields.Float(
        compute='_get_budget_kpi_new',
        readonly=False,
        store=True,
    )
    budget_percent = fields.Float(
        compute='_get_budget_percent',
        readonly=False,
        store=True,
    )

    @api.onchange("budget_kpi_old", "budget_percent")
    def _get_budget_new_api(self):
        for record in self:
            if record.budget_kpi_old:
                record.budget_kpi_new = record.budget_kpi_old * (1 + record.budget_percent)

    @api.onchange("budget_kpi_old", "budget_kpi_new")
    def _get_budget_percent(self):
        for record in self:
            if record.budget_kpi_old:
                if record.budget_kpi_old and record.budget_kpi_new:
                    record.budget_percent = record.budget_kpi_new / record.budget_kpi_old - 1
