{
    "name": "Self Service",
    "author": "Loym",
    "data": [
        "views/product_template_views.xml",
        "views/self_service_views.xml",
        "views/menus.xml",
        "security/ir.model.access.csv",
        "security/self_service_rules.xml",
    ],
    "depends": [
        "product",
        "sales_team",
        "web_widget_numeric_step",
    ],
    "license": "AGPL-3",
    "version": "16.0.1.0.0",
    'images': ['static/description/icon.svg'],
    "description": "Roadmap: Replace User with Analytic Account or Analytic Distribution.",
}
