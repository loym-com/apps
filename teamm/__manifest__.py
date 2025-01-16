# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Team M",
    "summary": "",
    "author": "Fredheim",
    "category": "Uncategorized",
    "data": [
        "security/ir.model.access.csv",
        "views/teamm_views.xml",
        "views/teamm_alias_views.xml",
        "views/teamm_model_views.xml",
        # "data/teamm.xml",
    ],
    "depends": [
        "event_sale_resource_booking",
        "event_sale_resource_booking_timeline",
        "hubspot_id",
        "partner_contact_birthdate",
        "partner_contact_gender",
        "partner_firstname",
        # "partner_product_price",
        "resource_booking_inverse",
        "resource_group",
        "sale_inverse",
        "sale_start_end_dates",
        "sale_start_end_dates_inverse",
        "website_event_sale_resource_booking", # resource.resource.combination_ids
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": [],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
}
