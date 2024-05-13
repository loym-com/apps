# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Worldline terminal",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "",
    "data": [
        "reports/pos_payment_terminal_log_reports.xml",
        "reports/pos_session_reports.xml",
        "views/point_of_sale_assets.xml",
        "views/pos_payment_method_views.xml",
    ],
    "depends": [
        "point_of_sale",
        "pos_payment_terminal_log",
    ],
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "qweb": [
        "static/src/xml/OrderReceipt.xml"
    ],
    "version": "14.0.1.0.0",
    "website": "https://github.com/",
}
