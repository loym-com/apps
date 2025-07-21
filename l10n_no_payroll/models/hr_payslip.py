import logging
from collections import defaultdict
from datetime import date, datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def action_l10n_no_fp_i_aar(self):
        self._action_l10n_no_fp("update_payslips", "this_year")

    def action_l10n_no_fp_i_fjor(self):
        self._action_l10n_no_fp("update_payslips", "last_year")

    def action_l10n_no_fp_i_aar_show(self):
        self._action_l10n_no_fp("show", "this_year")

    def action_l10n_no_fp_i_fjor_show(self):
        self._action_l10n_no_fp("show", "last_year")

    def action_l10n_no_fp_show(self):
        self._action_l10n_no_fp("show")

    def _action_l10n_no_fp(self, action, relative_year=None):
        """
        :param action: "show" or "update_payslips"
        :param relative_year: "this_year", "last_year" or None
        """

        # Get key variables
        fp_prosent = self.env.company.l10n_no_fp_prosent / 100
        fp_prosent_senior = self.env.company.l10n_no_fp_prosent_senior / 100
        loennsart_fp_i_aar = self.env.company.l10n_no_loennsart_fp_i_aar
        loennsart_fp_i_fjor = self.env.company.l10n_no_loennsart_fp_i_fjor

        # Get info from the payslip lines into dictinary 'd'
        d = defaultdict(dict)
        year_filter = None
        if relative_year:
            unique_employees = set(self.mapped("employee_id.id"))
            if len(unique_employees) != len(self):
                msg = (
                    "Each payslip should have a different employee. "
                    "There are {} payslips with {} unique employees."
                ).format(len(self), len(unique_employees))
                raise UserError(msg)

            unique_dates = set(self.mapped("date_from"))
            if len(unique_dates) != 1:
                raise UserError(f"There are multiple payslip dates: {unique_dates}")
            date_from = unique_dates.pop()

            if relative_year not in ["this_year", "last_year"]:
                raise UserError("Invalid year parameter.")
            year_filter = date_from.year if relative_year == "this_year" else date_from.year - 1
        #     domain = [
        #         ("date_from", ">=", datetime(year, 1, 1).date()),
        #         ("date_to", "<=", datetime(year, 12, 31).date()),
        #     ]
        # else:
        #     domain = []
        domain = []
        payslip_lines = self.search(domain).line_ids
        for line in payslip_lines:
            total = -line.total if line.credit_note else line.total
            employee_id = line.employee_id.id
            rule = line.salary_rule_id
            year = line.slip_id.date_to.year
            if rule == loennsart_fp_i_fjor:
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
            if rule in [loennsart_fp_i_fjor, loennsart_fp_i_aar]:
                d[employee_id]["year"][year]["paid"] += total
            elif line.salary_rule_id.l10n_no_BeregnFP:
                d[employee_id]["year"][year]["basis"] += total

        if action == "show":
            self._l10n_no_fp_show(d, year_filter)
        elif action == "update_payslips":
            if relative_year == "this_year":
                self._l10n_no_fp_update_payslips(d, relative_year, loennsart_fp_i_aar)
            elif relative_year == "last_year":
                self._l10n_no_fp_update_payslips(d, relative_year, loennsart_fp_i_fjor)
            else:
                raise UserError("Unknown relative year: {}".format(relative_year))
        else:
            raise UserError("Unknown action: {}".format(action))

    @api.model
    def _l10n_no_fp_show(self, d, year_filter=None):
        # Create a CSV report
        header = "unpaid,employee_id,employee_name,year,basis,rate,vacation_money,paid,unpaid"
        rows = []
        for employee_id in d:
            for year in d[employee_id]["year"]:
                if year_filter and year != year_filter:
                    continue
                vacation_money = (
                    d[employee_id]["year"][year]["basis"]
                    * d[employee_id]["year"][year]["rate"]
                )
                unpaid = vacation_money - d[employee_id]["year"][year]["paid"]
                # pattern = "%.2f,%s,%s,%s,%.2f,%.3f,%.2f,%.2f,%.2f\n"
                pattern = "%.2f,%s,%s,%s,%s,%s,%.2f,%.2f,%.2f"
                rows.append(
                    [
                        round(unpaid, 2),
                        employee_id,
                        d[employee_id]["name"],
                        year,
                        round(d[employee_id]["year"][year]["basis"], 2),
                        d[employee_id]["year"][year]["rate"],
                        round(vacation_money, 2),
                        round(d[employee_id]["year"][year]["paid"], 2),
                        round(unpaid, 2),
                    ]
                )
        # Sort by second column (employee_id)
        sorted_rows = sorted(rows, key=lambda row: row[2])
        # Build CSV string
        csv_lines = [header] + [",".join(str(x) for x in row) for row in sorted_rows]
        csv_string = "\n".join(csv_lines)
        raise UserError(csv_string)

    def _l10n_no_fp_update_payslips(self, d, relative_year, loennsart):
        year = self[0].date_from.year
        if relative_year == "last_year":
            year -= 1

        for payslip in self:
            if payslip.state not in ["draft", "verify"]:
                raise UserError("Payslip must be in draft or verify state.")
            values = d[payslip.employee_id.id]["year"][year]
            vacation_money = values["basis"] * values["rate"]
            unpaid = round(vacation_money - values["paid"], 2)
            if not unpaid:
                continue

            line = payslip.line_manually_ids.filtered(
                lambda l: l.salary_rule_id.id == loennsart.id)
            if line:
                if len(line) > 1:
                    raise UserError("Multiple lines for the same salary rule.")
                if not line.quantity == 1.0:
                    raise UserError("Quantity must be 1.0 for vacation money.")
                if not line.rate == 100.0:
                    raise UserError("Rate must be 100.0 for vacation money.")
                line.amount += unpaid
            else:
                # Create a new line for vacation money
                self.env["hr.payslip.line.manually"].create({
                    "model": "hr.payslip",
                    "res_id": payslip.id,
                    "salary_rule_id": loennsart.id,
                    "quantity": 1.0,
                    "rate": 100.0,
                    "amount": unpaid,
                })
            payslip.compute_sheet()
