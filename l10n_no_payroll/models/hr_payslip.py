import logging
from collections import defaultdict
from datetime import date, datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    """
    Feriepenger menuitem:
        payslip_lines: all
        action: show feriepenger

    Payslip run action:
        Feriepenger forrige år
            payslip_lines: last year
            action: show feriepenger not paid

    Payslips actions:
        Feriepenger forrige år
            payslip_lines: last year for payslip employees
            action: update payslips
        Feriepenger inneværende år
            payslip_lines: this year for payslip employees
            action: update payslips

    Show feriepenger:
        2 decimals
        Show what to pay in first column
    """

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
            date_from = self.mapped("date_from")
            assert len(date_from) == 1, "Only one payslip period allowed."
            assert relative_year in ["this_year", "last_year"], "Invalid year parameter."
            date_from = date_from[0]
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
        csv = "unpaid,employee_id,employee_name,year,basis,rate,vacation_money,paid,unpaid\n"
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
                pattern = "%.2f,%s,%s,%s,%s,%s,%.2f,%.2f,%.2f\n"
                csv += pattern % (
                    unpaid,
                    employee_id,
                    d[employee_id]["name"],
                    year,
                    d[employee_id]["year"][year]["basis"],
                    d[employee_id]["year"][year]["rate"],
                    vacation_money,
                    d[employee_id]["year"][year]["paid"],
                    unpaid,
                )
        raise UserError(csv)

    def _l10n_no_fp_update_payslips(self, d, relative_year, loennsart):
        year = self[0].date_from.year
        if relative_year == "last_year":
            year -= 1

        for payslip in self:
            assert payslip.state in ["draft", "verify"], "Payslip must be in draft or verify state."
            values = d[payslip.employee_id.id]["year"][year]
            vacation_money = values["basis"] * values["rate"]
            unpaid = round(vacation_money - values["paid"], 2)
            if not unpaid:
                continue

            line = payslip.line_manually_ids.filtered(
                lambda l: l.salary_rule_id.id == loennsart.id)
            if line:
                assert len(line) == 1, "Multiple lines for the same salary rule."
                assert line.quantity == 1.0, "Quantity must be 1.0 for vacation money."
                assert line.rate == 100.0, "Rate must be 100.0 for vacation money."
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
