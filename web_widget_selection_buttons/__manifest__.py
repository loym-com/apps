{
    'name': 'Selection Buttons OWL16',
    'version': '16.0.1.0.0',
    'category': 'Custom',
    'summary': 'Vis selection-felt som knapper med OWL2',
    'author': 'Din Navn',
    'depends': ['base', 'web', "multi_step_wizard"],
    'data': [
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
        "wizards/my_wizard_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'web_widget_selection_buttons/static/src/js/selection_buttons.js',
            'web_widget_selection_buttons/static/src/xml/selection_buttons_template.xml',
        ],
    },
    'installable': True,
    'application': False,
}
