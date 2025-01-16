# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Online Events with Resource Booking",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Appointments",
    "data": [
        "security/ir.model.access.csv",
        "views/website_event_booking_combination_views.xml",
        "views/website_event.xml",
        # "views/website_sale.xml",
    ],
    "depends": [
        # "base_set_record_values_mixin",
        # "product_attribute_value_tag",
        "event_sale_resource_booking",
        "website_event_sale",
        "website_sale_filter",  # depends on website_sale_product_variant
        # "website_sale_product_variant",
        # "website_sale_resource_booking",
    ],
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "post_init_hook": "post_init_hook",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
}
