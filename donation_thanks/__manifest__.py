# Copyright 2022-2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Donation Thanks",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Accounting & Finance",
    "data": [
        "data/report_paperformat_data.xml", # before reports
        "data/ir_actions_report_data.xml",
        "data/res_partner_category_data.xml", # before mail templates
        "data/mail_template_data.xml", # before server actions
        "data/ir_actions_server_data.xml",
        "reports/report_donation_thanks_templates.xml",
        "views/donation_tax_receipt_views.xml",
        "views/donation_thanks_template_views.xml",
        "views/ir_attachment_views.xml",
        "views/res_partner_views.xml",
    ],
    "depends": [
        # "base_partner_family",
        "donation",
        "donation_analytic",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/donation",
}
