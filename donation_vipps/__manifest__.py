{
    "name": "[DEV] Donation Vipps",
    "summary": "Store raw Vipps webhook requests for inspection in Odoo.",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Accounting & Finance",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/vipps_webhook_views.xml",
        "views/donation_vipps_menu.xml",
    ],
}
