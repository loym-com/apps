# Copyright 2019 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Payslip Line with more fields",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "auto_install": False,
    "category": "Uncategorized",
    "data": [
        "views/hr_payslip_line_views.xml",
    ],
    "depends": ["payroll"],
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "pre_init_hook": "pre_init_hook",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA",
}
