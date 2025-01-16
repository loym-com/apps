# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "See events in booking timeline",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Appointments",
    "data": [
        "data/data.xml",
        "views/event_event_views.xml",
    ],
    "depends": [
        "event_sale_resource_booking",
        "resource_booking_timeline",
    ],
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/sale-workflow",
}
