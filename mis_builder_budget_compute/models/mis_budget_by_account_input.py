from odoo import _, api, fields, models


class AccountAccountTag(models.Model):
    _name = "mis.budget.by.account.input"
    _description = "Input for action_compute_budget_items()"

    # This model is used by mis.budget.by.account action_compute_budget_items().

    account_tag_id = fields.Many2one("account.account.tag")
    # TODO? Other possible implementations:
    # account_group_id = fields.Many2one("account.group")
    # account_id = fields.Many2one("account.account")

    date_range_id = fields.Many2one("date.range")
    kpi_old = fields.Float()
    kpi_new = fields.Float(
        compute='_get_kpi_new',
        readonly=False,
        store=True,
    )
    percent = fields.Float(
        compute='_get_percent',
        readonly=False,
        store=True,
        help="Percent increase (New KPI / Old KPI - 1)"
    )

    @api.onchange("kpi_old", "percent")
    def _get_kpi_new(self):
        for record in self:
            if record.kpi_old:
                record.kpi_new = record.kpi_old * (1 + record.percent)

    @api.onchange("kpi_old", "kpi_new")
    def _get_percent(self):
        for record in self:
            if record.kpi_old:
                if record.kpi_old and record.kpi_new:
                    record.percent = record.kpi_new / record.kpi_old - 1
