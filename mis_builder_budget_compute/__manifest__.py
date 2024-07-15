# Copyright 2023 appstogrow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Compute a budget",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-financial-reporting",
    "category": "Localization",
    "depends": [
        "base_set_record_values_mixin",
        "mis_builder_budget",
        "web_widget_x2many_2d_matrix",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_account_tag_views.xml",
        "views/mis_budget_by_account_views.xml",
        "views/mis_budget_by_account_item_views.xml",
        # "views/mis_budget_by_account_item_views.xml",
    ],
    "maintainers": ["norlinhenrik"],
}
