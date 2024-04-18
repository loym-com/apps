# Copyright 2023 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Resource Booking Demo",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Uncategorized",
    "data": [
        "data/demo.xml",
        "views/resource_booking_views.xml",
    ],
    "depends": [
        "contacts",  # optional
        # "payment_custom",  # optional
        "sale_management",  # optional
        # "web_responsive",  # optional oca/web
        "website_sale_resource_booking",  # oca/calendar, oca/sale-workflow, oca/e-commerce
        "partner_product_price",  # oca/product-attribute
        "resource_booking_timeline",
        "sale_resource_booking_period",
        "sale_product_pack",  # oca/product-pack
        "product_pack_template",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
}
