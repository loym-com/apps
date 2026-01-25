# Copyright 2019-2023 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Skattefradrag for gaver",
    "summary": "",
    "version": "16.0.1.0.0",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Localization",
    "data": [
        "security/ir.model.access.csv",
        # "data/data.xml",
        "views/views.xml",
    ],
    "depends": [
        "donation",  # OCA/donation
        # "partner_identification",  # OCA/partner-contact - use with donation_tax_receipt_advanced.py
        "partner_contact_id",  # invisible for companies
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "website": "https://github.com/OCA",
}
