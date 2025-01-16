# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sell Event with Resource Booking",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Appointments",
    "data": [
        "data/data.xml",
        "views/event_event_views.xml",
        "views/event_registration_views.xml",
        "views/product_template_views.xml",
        "views/resource_booking_views.xml",
        "views/sale_order_line_views.xml",
        "views/sale_order_views.xml",
    ],
    "depends": [
        "event",
        "sale_resource_booking",
    ],
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/sale-workflow",
}
