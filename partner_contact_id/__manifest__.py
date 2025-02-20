# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Contact Identification Number",
    "summary": "Add ID field to contacts",
    "version": "15.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": ["partner_contact_personal_information_page"],
    "data": ["views/res_partner.xml"],
}
