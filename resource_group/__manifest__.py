
{
    "name": "Resource Group",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "data": [
        "security/ir.model.access.csv",
        "views/resource_group_tag_views.xml",
        "views/resource_group_views.xml",
        "views/resource_resource_views.xml",
    ],
    "depends": [
        "resource",
        "resource_booking", # compute resource.booking.combination name
    ],
    "version": "1.0",
    "license": "AGPL-3",
}
