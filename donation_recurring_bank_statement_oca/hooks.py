from odoo import api, SUPERUSER_ID

def uninstall_hook(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref("donation.donation_line_action").domain = []
