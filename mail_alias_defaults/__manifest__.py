# Copyright 2022 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Mail Alias Compute Defaults",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Mail",
    "data": [
        "views/mail_alias_view.xml",
    ],
    "depends": [
        "base_time_parameter",
        "mail",
    ],
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "pre_init_hook": "pre_init_hook",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA",
}
