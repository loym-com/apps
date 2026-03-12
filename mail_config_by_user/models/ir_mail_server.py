from odoo import api, fields, models, tools, _


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    smtp_user = fields.Char(groups=False)
    smtp_pass = fields.Char(groups=False)
    smtp_ssl_certificate = fields.Binary(groups=False)
    smtp_ssl_private_key = fields.Binary(groups=False)

    def test_smtp_connection(self):
        values = set(
            self.from_filter,
            self.smtp_user,
            self.env.user.login,
        )
        if len(values) == 1:
            # The user is testing its own connection.
            # Use sudo to allow access to the credentials.
            return super(IrMailServer, self.sudo()).test_smtp_connection()
        else:
            return super().test_smtp_connection()
