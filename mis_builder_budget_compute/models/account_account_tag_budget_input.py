from odoo import _, api, fields, models


class AccountAccountTag(models.Model):
    _name = "account.account.tag.budget.input"
    _description = "Account or Tag input for action_compute_budget_items()"

    # This model is used by mis.budget.by.account action_compute_budget_items().

    account_tag_id = fields.Many2one("account.account.tag")
    # TODO? Other possible implementations:
    # account_group_id = fields.Many2one("account.group")
    # account_id = fields.Many2one("account.account")

    date_range_id = fields.Many2one("date.range")
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
        help="Percent increase (New KPI / Old KPI - 1)"
    )

    @api.onchange("budget_kpi_old", "budget_percent")
    def _get_budget_kpi_new(self):
        for record in self:
            if record.budget_kpi_old:
                record.budget_kpi_new = record.budget_kpi_old * (1 + record.budget_percent)

    @api.onchange("budget_kpi_old", "budget_kpi_new")
    def _get_budget_percent(self):
        for record in self:
            if record.budget_kpi_old:
                if record.budget_kpi_old and record.budget_kpi_new:
                    record.budget_percent = record.budget_kpi_new / record.budget_kpi_old - 1
