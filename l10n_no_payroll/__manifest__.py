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
        "data/l10n_no_job_code.xml",
        "data/l10n_no_tabelltrekk.xml",
    ],
    "demo": [
        # "demo/hr_contribution_register_data.xml",
        "demo/hr_salary_rule_category_data.xml",
        "demo/hr_salary_rule_data.xml",
        "demo/hr_payroll_structure_data.xml",
    ],
    "depends": [
        "base_sparse_field",
        "hr_contract_leave",
        "l10n_no_oca",
        "payroll_account_analytic",
        # "payroll_custom_info",
    ],
    "external_dependencies": {"python": ["pyxb"]},
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "15.0.1.0.0",
    "website": "https://github.com/OCA",
}
