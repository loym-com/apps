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
        self._l10n_no_feriepenger("update_payslips", "this_year")

    def action_l10n_no_fp_i_fjor(self):
        self._l10n_no_feriepenger("update_payslips", "last_year")

    def action_l10n_no_fp_i_fjor_csv(self):
        self._l10n_no_feriepenger("show", "last_year")

    def action_l10n_no_fp_csv(self):
        self._l10n_no_feriepenger("show")

    def _l10n_no_feriepenger(self, action, year=None):

        # Get key variables
        fp_prosent = self.env.company.l10n_no_fp_prosent / 100
        fp_prosent_senior = self.env.company.l10n_no_fp_prosent_senior / 100
        loennsart_fp_i_aar_id = self.env.company.l10n_no_loennsart_fp_i_aar
        loennsart_fp_i_fjor_id = self.env.company.l10n_no_loennsart_fp_i_fjor

        # Get info from the payslip lines into dictinary 'd'
        d = defaultdict(dict)
        if year:
            date_from = self.mapped("date_from")
            assert len(date_from) == 1, "Only one payslip period allowed."
            assert year in ["this_year", "last_year"], "Invalid year parameter."
            year = date_from.year if year == "this_year" else date_from.year - 1
            domain = [
                ("date_from", ">=", datetime(year, 1, 1).date()),
                ("date_to", "<=", datetime(year, 12, 31).date()),
            ]
        else:
            domain = []
        payslip_lines = self.search(domain)
        for line in payslip_lines:
            total = -line.total if line.credit_note else line.total
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
                d[employee_id]["year"][year]["paid"] += total
            elif line.salary_rule_id.l10n_no_BeregnFP:
                d[employee_id]["year"][year]["basis"] += total

        if action == "csv":
            # Create a CSV report
            csv = "employee_id,employee_name,year,basis,rate,vacation_money,paid,unpaid\n"
            for employee_id in d:
                for year in d[employee_id]["year"]:
                    vacation_money = (
                        d[employee_id]["year"][year]["basis"]
                        * d[employee_id]["year"][year]["rate"]
                    )
                    unpaid = vacation_money - d[employee_id]["year"][year]["paid"],
                    csv += "%.2f,%s,%s,%s,%.2f,%.3f,%.2f,%.2f,%.2f\n" % (
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
        elif action == "update_payslips":
            for payslip in self:
                pass
        else:
            raise UserError("Unknown action: {}".format(action))

