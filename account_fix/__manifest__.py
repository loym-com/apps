# Copyright 2019 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Fix",
    "summary": "Journal Sequence",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Administration",
    "data": [
        "views/account_bank_statement_line.xml",
        "views/account_journal.xml",
        "views/account_move.xml",
        "views/account_move_line.xml",
        "views/res_company.xml",
    ],
    "depends": [
        "account",
        # "account_financial_report",
        "account_reconcile_oca",
    ],
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA",
}
