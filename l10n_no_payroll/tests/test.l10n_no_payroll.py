import logging
from datetime import datetime

from .common import TestNoPayrollBase

_logger = logging.getLogger(__name__)


class TestNoPayroll(TestNoPayrollBase):
    def setUp(self):
        super().setUp()

        self.TaxDeduction = self.env["l10n.no.tabelltrekk"]
        self.JobCode = self.env["l10n.no.job.code"]

    def test_00_post_init_hook(self):
        tax_deduction_count = self.TaxDeduction.search_count([])
        self.assertGreater(tax_deduction_count, 200000)

        job_code_count = self.JobCode.search_count([])
        self.assertGreater(job_code_count, 6000)

    def test_10_workflow(self):
        # Archive all employees except for one
        self.env["hr.employee"].search([("id", "!=", self.employee.id)]).active = False

        payslip = self.env["hr.payslip"].create(
            [
                {
                    "employee_id": self.employee.id,
                    "contract_id": self.contract.id,
                    "date_from": datetime(2023, 1, 1).date(),
                    "date_to": datetime(2023, 1, 31).date(),
                    "struct_id": self.env.ref("l10n_no_payroll.structure_no").id,
                },
            ]
        )
        payslip.compute_sheet()
        self.assertEqual(payslip.get_salary_line_total("NET"), 33450 - 31100 * 0.32)

        amelding_wizard = self.env["l10n.no.amelding.wizard"].create(
            [
                {
                    "kalendermaaned": "2023-01",
                }
            ]
        )
        amelding_wizard.lag_amelding()
        _logger.info("TODO: display the content of the amelding XML file ...")
