# Copyright 2021 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Ows Multicompany Security",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Uncategorized",
    "data": [
        "server_actions.xml",
    ],
    "depends": [
        "base",
        "product",
        "auth_password_policy_signup",
        "multicompany_base",
    ],
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com",
}
