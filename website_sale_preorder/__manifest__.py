{
    "name": "Website Sale Preorder",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
    "category": "Website/Website",
    "depends": ["website_sale"],
    "data": [
        "data/ir_model_data.xml",
        "views/product_template_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "application": False,
    'assets': {
        'website.assets_editor': [
            'website_sale_preorder/static/src/js/website_sale_form_editor.js',
        ],
    },
}
