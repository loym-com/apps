{
    "name": "[ERROR: CANNOT INSTALL NEW APPS] Base Search Order",
    "version": "16.0.1.0.0",
    "category": "Tools",
    "summary": "Allow DB admins to define default search order per model",
    "author": "Loym",
    "depends": ["base"],
    "data": [
        "views/ir_model_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
    "application": False,
    "pre_init_hook": "pre_init_hook",
}
