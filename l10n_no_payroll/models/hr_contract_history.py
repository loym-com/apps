from odoo import fields, models


class HrContractHistory(models.Model):
    _inherit = "hr.contract.history"

    def action_l10n_no_create_fp_contract(self):
        last_contract = self.contract_ids.sorted("date_start", reverse=True)[:1]
        values = {
            "name": "{} - feriepenger".format(self.employee_id.name),
            "employee_id": self.employee_id.id,
            "date_start": fields.Date.today(),
            "date_end": fields.Date.today(),
            "job_id": last_contract.job_id.id,
            "hr_responsible_id": last_contract.hr_responsible_id.id,
            "struct_id": last_contract.struct_id.id,
            "analytic_account_id": last_contract.analytic_account_id.id,
            "journal_id": last_contract.journal_id.id,
            "l10n_no_Arbeidsforholdtype": "pensjonOgAndreTyperYtelserUtenAnsettelsesforhold",
            "l10n_no_Arbeidstidsordning": False,
            "l10n_no_antallTimerPerUkeSomEnFullStillingTilsvarer": 0.0,
            "wage": 0.0,
            "state": "open",
        }
        new_contract = self.env["hr.contract"].create(values)
