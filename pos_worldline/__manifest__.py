# Copyright 2024 Stiftelsen Hjertegod - Fredheim Livsstilssenter

{
    "name": "Worldline terminal",
    "summary": "",
    "author": "Henrik Norlin",
    "category": "",
    'assets': {
        "point_of_sale.assets": [
            "pos_worldline/static/src/js/models.js",
            "pos_worldline/static/src/js/payment_worldline.js",
            "pos_worldline/static/src/xml/OrderReceipt.xml",
        ],
    },
    "data": [
        "reports/pos_payment_terminal_log_reports.xml",
        "reports/pos_session_reports.xml",
        "views/pos_payment_method_views.xml",
    ],
    "depends": [
        "point_of_sale",
        "pos_payment_terminal_log",
        "web_notify",
    ],
    "license": "Other proprietary",
    "maintainers": ["norlinhenrik"],
    "version": "16.0.1.0.0",
    "website": "https://fredheim.org",
}
