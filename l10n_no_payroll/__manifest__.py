# Copyright 2019-2023 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Norway - Payroll",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Localization",
    "data": [
        "security/ir.model.access.csv",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_job_views.xml",
        "views/hr_leave_type_views.xml",
        "views/hr_leave_views.xml",
        "views/hr_payslip_views.xml",
        "views/hr_payslip_run_views.xml",
        "views/hr_salary_rule_views.xml",
        "views/l10n_no_amelding_views.xml",
        "views/l10n_no_amelding_wizard_views.xml",
        "views/res_company_views.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/hr_salary_rule_demo.xml",
        "demo/hr_payroll_structure_demo.xml",
        "demo/res_company_demo.xml",
    ],
    "depends": [
        "base_import",  # l10n_no_job_code
        "base_sparse_field",
        "hr_contract_leave",
        "l10n_no",
        "payroll_account_analytic",
    ],
    "external_dependencies": {"python": ["xsdata-pydantic"]},
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "post_init_hook": "post_init_hook",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA",
}
