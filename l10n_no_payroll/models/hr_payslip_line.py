import logging
from collections import defaultdict
from datetime import datetime, date

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

    @api.model
    def l10n_no_feriepenger(self):

        # Get key variables
        fp_prosent = self.env.company.l10n_no_fp_prosent / 100
        fp_prosent_senior = self.env.company.l10n_no_fp_prosent_senior / 100
        loennsart_fp_i_aar_id = self.env.company.l10n_no_loennsart_fp_i_aar
        loennsart_fp_i_fjor_id = self.env.company.l10n_no_loennsart_fp_i_fjor

        # Get info from the payslip lines into dictinary 'd'
        d = defaultdict(dict)
        payslip_lines = self.search([("date_from", "<", date(2024, 1, 1))])
        for line in payslip_lines:
            employee_id = line.employee_id.id
            rule = line.salary_rule_id
            year = line.slip_id.date_to.year
            if rule == loennsart_fp_i_fjor_id:
                year -= 1

            if not employee_id in d:
                d[employee_id]["name"] = line.employee_id.name
                if not line.employee_id.birthday:
                    raise UserError("Please register birthdate for {}.".format(
                        line.employee_id.name
                    ))
                d[employee_id]["birthyear"] = line.employee_id.birthday.year
                d[employee_id]["year"] = {}
            if not year in d[employee_id]["year"]:
                d[employee_id]["year"][year] = {
                    "basis": 0,
                    "rate": 0,
                    "vacation_money": 0,
                    "paid": 0,
                }
                # Senior rate the year before the worker becomes 60 years old
                if year - d[employee_id]["birthyear"] >= 59:
                    d[employee_id]["year"][year]["rate"] = fp_prosent_senior
                else:
                    d[employee_id]["year"][year]["rate"] = fp_prosent
            if rule in [loennsart_fp_i_fjor_id, loennsart_fp_i_aar_id]:
                d[employee_id]["year"][year]["paid"] += line.total
            elif line.salary_rule_id.l10n_no_BeregnFP:
                d[employee_id]["year"][year]["basis"] += line.total

        # Create a CSV report
        csv = "employee_id,employee_name,year,basis,rate,vacation_money,paid,unpaid\n"
        for employee_id in d:
            for year in d[employee_id]["year"]:
                vacation_money = (
                    d[employee_id]["year"][year]["basis"]
                    * d[employee_id]["year"][year]["rate"]
                )
                csv += "%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    employee_id,
                    d[employee_id]["name"],
                    year,
                    d[employee_id]["year"][year]["basis"],
                    d[employee_id]["year"][year]["rate"],
                    vacation_money,
                    d[employee_id]["year"][year]["paid"],
                    vacation_money - d[employee_id]["year"][year]["paid"],
                )

        raise UserError(csv)
