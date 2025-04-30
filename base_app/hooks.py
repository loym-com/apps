from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    apps = env["ir.module.module"].search([])
    apps.import_prices()
