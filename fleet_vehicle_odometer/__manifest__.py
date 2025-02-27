# Copyright 2019 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Fleet vehicle odometer",
    "summary": "Analytic Fleet",
    "author": "Ows, Odoo Community Association (OCA)",
    "auto_install": True,
    "category": "Administration",
    "data": [
        "views/fleet_vehicle_views.xml",
        "views/fleet_vehicle_odometer_views.xml",
    ],
    "depends": [
        "analytic",
        "fleet",
    ],
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA",
}
