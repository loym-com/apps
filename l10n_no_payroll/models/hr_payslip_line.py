import logging
from collections import defaultdict
from datetime import date, datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    l10n_no_man_months = fields.Float(
        "Man Months", compute="_compute_man_months", store=True, default=lambda self: self._compute_man_months(),
    )
    l10n_no_total_ytd = fields.Float(
        "Total, year to date", compute="_compute_l10n_no_total_ytd"
    )

    @api.depends(
        "salary_rule_id.l10n_no_Loennsbeskrivelse",
        # "l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer",
        "quantity",
        "rate",
    )
    def _compute_man_months(self):
        for line in self:
            code = line.salary_rule_id.l10n_no_Loennsbeskrivelse
            if code == "fastloenn":
                line.l10n_no_man_months = line.quantity * line.rate / 100.0
            elif code == "timeloenn":
                # hours_per_week = line.l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer
                # TODO: Get hours per week from the hr.contract. How, when the payslip.contract_id is empty?
                hours_per_week = 37.5
                weeks_per_year = 52.0
                months_per_year = 12.0
                hours_per_month = (
                    float(hours_per_week) * weeks_per_year / months_per_year
                )
                line.l10n_no_man_months = (
                    line.quantity * line.rate / 100.0 / hours_per_month
                )
            else:
                line.l10n_no_man_months = 0.0
            if len(self) == 1:
                return line.l10n_no_man_months

    def _compute_l10n_no_total_ytd(self):
        for line in self:
            date_from = line.slip_id.date_from
            lines_ytd = self.search(
                [
                    ("employee_id", "=", line.employee_id.id),
                    ("salary_rule_id", "=", line.salary_rule_id.id),
                    ("date_from", ">=", datetime(date_from.year, 1, 1).date()),
                    ("date_from", "<=", date_from),
                ]
            )
            line.l10n_no_total_ytd = sum(lines_ytd.mapped("total"))
