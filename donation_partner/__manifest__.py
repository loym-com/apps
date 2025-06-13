# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Donation Partner",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Accounting & Finance",
    "data": [
        "data/ir_actions_server_data.xml",
        # "views/donation_donation_views.xml",
        # "views/donation_tax_receipt_views.xml",
        "views/res_partner_views.xml",
    ],
    "depends": [
        "donation_thanks",
        "partner_valid_postal_address",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/donation",
}
