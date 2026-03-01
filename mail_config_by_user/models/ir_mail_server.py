from odoo import api, fields, models, tools, _


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    smtp_user = fields.Char(groups=False)
    smtp_pass = fields.Char(groups=False)
    smtp_ssl_certificate = fields.Binary(groups=False)
    smtp_ssl_private_key = fields.Binary(groups=False)
