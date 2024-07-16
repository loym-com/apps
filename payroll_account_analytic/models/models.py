import logging

from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)


class HrPayslipRun(models.Model):
    _inherit = "hr.payslip.run"

    def test_payslip_accounting(self):
        self.ensure_one()
        account_moves = self.slip_ids.test_payslip_accounting(
            hr_payslip_run_name=self.name
        )
        return {
            "name": "Payroll Moves",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", [move.id for move in account_moves]]],
        }

    def confirm_payslip_accounting(self):
        self.ensure_one()
        account_moves = self.slip_ids.confirm_payslip_accounting(
            hr_payslip_run_name=self.name
        )
        self.write({"state": "close"})
        return {
            "name": "Payroll Moves",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", [move.id for move in account_moves]]],
        }


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def test_payslip_accounting(self, hr_payslip_run_name=None):
        """
        Delete unposted moves related to payslips in the batch
        Skip payslips with posted move
        Create one move (per journal/month) with totals for the batch/journal/month
            account_move.ref = _('Payroll')
            account_move_line.name = hr_payslip_run_name or "/"
            account_move_line.narration = ""
        Set move_id & date on the payslips
        """
        _logger.debug("hr_payslip_run_name = " + str(hr_payslip_run_name))
        # check
        for slip in self:
            if not slip.journal_id:
                raise UserError(_("Slip %s should have a journal!" % (slip.ref)))
            if not slip.date and not slip.date_to:
                raise UserError(_('Slip %s needs "date" or "date_to"!' % (slip.ref)))

        # delete account.move (if not posted)
        # group payslips per journal/month (skip if posted)
        grouped_payslips = []
        for slip in self:
            if slip.move_id:
                if slip.move_id.state == "posted":
                    continue
                else:
                    self.env["account.move"].browse(slip.move_id.id).unlink()
            date = slip.date or slip.date_to
            year_month = date.strftime("%Y-%m")
            appended = False
            for group in grouped_payslips:
                if (
                    group["journal_id"] == slip.journal_id.id
                    and group["month"] == year_month
                ):
                    group["payslips"].append(slip.id)
                    group["date_to"] = max(group["date_to"], slip.date or slip.date_to)
                    appended = True
            if not appended:
                grouped_payslips.append(
                    {
                        "journal_id": slip.journal_id.id,
                        "month": year_month,
                        "payslips": [slip.id],
                        "date_to": date,
                    }
                )

        # TODO: Move to l10n_no_payroll
        company = self.env.company
        aga = float(company.l10n_no_Grunnlagsprosent) / 100.0
        fp = company.l10n_no_fp_prosent / 100.0
        fp_senior = company.l10n_no_fp_prosent_senior / 100.0

        # create one account.move per journal/month
        # update payslip.move_id & payslip.date
        precision = self.env["decimal.precision"].precision_get("Payroll")
        account_moves = []
        for group in grouped_payslips:
            account_move_lines = []
            total = 0.0
            name = hr_payslip_run_name or "/"
            move_dict = {
                "ref": _("Payroll"),
                "journal_id": group["journal_id"],
                "date": group["date_to"],
            }

            for slip in self.browse(group["payslips"]):
                if not hr_payslip_run_name:
                    move_dict = {
                        "ref": slip.number,
                        "journal_id": slip.journal_id.id,
                        "date": group["date_to"],
                    }
                contract_analytic_account_id = None
                if slip.contract_id and slip.contract_id.analytic_account_id:
                    contract_analytic_account_id = (
                        slip.contract_id.analytic_account_id.id
                    )

                line_ids = slip.line_ids
                for line in line_ids:
                    amount = slip.credit_note and -line.total or line.total
                    if float_is_zero(amount, precision_digits=precision):
                        continue

                    def _add(new_amount, new_account, new_partner_id=False):
                        # Also using these variables:
                        # precision
                        # line
                        # contract_analytic_account_id
                        # name
                        # slip
                        # group
                        # account_move_lines
                        new_amount = float_round(new_amount, precision_digits=precision)
                        if new_account.include_initial_balance:
                            new_analytic_account_id = None
                        else:
                            new_analytic_account_id = (
                                line.analytic_account_id.id
                                or line.salary_rule_id.analytic_account_id.id
                                or contract_analytic_account_id
                            )
                        new = {
                            "name": name,
                            "partner_id": new_partner_id,
                            "account_id": new_account.id,
                            "journal_id": slip.journal_id.id,
                            "analytic_distribution": {},
                            "date": group["date_to"],
                            "amount": new_amount,
                            "tax_line_id": line.salary_rule_id.account_tax_id.id,
                        }
                        if new_analytic_account_id:
                            new["analytic_distribution"] = {str(new_analytic_account_id): 100}
                        compare = "start"
                        for aml in account_move_lines:
                            compare = "same"
                            for key in [
                                "name",
                                "partner_id",
                                "account_id",
                                "analytic_distribution",
                                "tax_line_id",
                            ]:
                                if aml[key] != new[key]:
                                    compare = "different"
                                    break
                            if compare == "same":
                                aml["amount"] += new_amount
                                break
                        if compare != "same":
                            account_move_lines.append(new)

                    debit_account = line.salary_rule_id.account_debit
                    if debit_account:
                        partner_id = line._get_partner_id(credit_account=False)
                        _add(amount, debit_account, partner_id)
                        total += amount

                    credit_account = line.salary_rule_id.account_credit
                    if credit_account:
                        partner_id = line._get_partner_id(credit_account=True)
                        _add(-amount, credit_account, partner_id)
                        total -= amount

                    if self.env.company.partner_id.country_id.code == "NO":
                        # TODO: move to a method in l10n_no_payroll; call the method from here (depends on def _add)

                        beregn_aga = line.salary_rule_id.l10n_no_BeregnAga
                        beregn_fp = line.salary_rule_id.l10n_no_BeregnFP

                        if beregn_aga:
                            _add(amount * aga, company.l10n_no_aga_konto)
                            _add(-amount * aga, company.l10n_no_aga_motkonto)
                        if beregn_fp:
                            year = line.slip_id.date_to.year
                            birthyear = line.employee_id.birthday.year
                            if year - birthyear >= 59:
                                fp = fp_senior
                            _add(amount * fp, company.l10n_no_fp_konto)
                            _add(-amount * fp, company.l10n_no_fp_motkonto)
                            _add(amount * aga * fp, company.l10n_no_aga_fp_konto)
                            _add(-amount * aga * fp, company.l10n_no_aga_fp_motkonto)

                        if line.salary_rule_id in (
                            company.l10n_no_loennsart_fp_i_aar,
                            company.l10n_no_loennsart_fp_i_fjor,
                        ):
                            _add(-amount * aga, company.l10n_no_aga_fp_konto)
                            _add(amount * aga, company.l10n_no_aga_fp_motkonto)

            if not float_is_zero(total, precision_digits=precision):
                acc_journal = self.env["account.journal"].browse(group["journal_id"])
                acc_id = acc_journal.default_account_id.id
                if not acc_id:
                    raise UserError(
                        _(
                            'The Expense Journal "%s" has not properly configured the Default Account!'
                        )
                        % (acc_journal.name)
                    )
                account_move_lines.append(
                    {
                        "name": name,
                        "account_id": acc_id,
                        "journal_id": acc_journal.id,
                        "date": group["date_to"],
                        "amount": -total,
                    }
                )

            for aml in account_move_lines:
                if aml["amount"] > 0:
                    aml["debit"] = aml["amount"]
                elif aml["amount"] < 0:
                    aml["credit"] = -aml["amount"]
                del aml["amount"]
            account_move_lines = [(0, 0, aml) for aml in account_move_lines]
            move_dict["line_ids"] = account_move_lines
            move = self.env["account.move"].create(move_dict)
            account_moves.append(move)
            for slip in self.browse(group["payslips"]):
                slip.write({"move_id": move.id, "date": group["date_to"]})

        return account_moves

    def confirm_payslip_accounting(self, hr_payslip_run_name=None):
        account_moves = self.test_payslip_accounting(hr_payslip_run_name)
        for move in account_moves:
            move.post()
        for slip in self:
            slip.write({"state": "done"})
        return account_moves

    def action_payslip_done(self):
        return self.confirm_payslip_accounting()
