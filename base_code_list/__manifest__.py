# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "Code Lists",
    "version": "16.0.1.0.0",
    "category": "Tools",
    "license": "LGPL-3",
    "development_status": "Production/Stable",
    "summary": "Base module for code lists",
    "author": "FIQ, Odoo Community Association (OCA)",
    "maintainers": ["norlinhenrik"],
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/code_list_views.xml",
        "views/code_list_item_views.xml",
        "views/code_list_usage_views.xml",
        "views/res_partner_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
}
