# Copyright 2026 Loym - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Web CSS",
    "summary": "Customize colors etc.",
    "author": "Loym, Odoo Community Association (OCA)",
    "category": "Administration",
    "data": ["views/res_config_settings.xml"],
    "depends": [
        "base_setup", # Settings
        "web_editor", # Assets
    ],
    "license": "AGPL-3",
    'uninstall_hook': "uninstall_hook",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA",
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'web_css/static/src/scss/variables.scss'),
        ],
        'web.assets_backend': [
            ('append', 'web_css/static/src/scss/backend.scss'),
        ],
    }
}
