from odoo import api, fields, models, tools, _


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    smtp_user = fields.Char(groups=False)
    smtp_pass = fields.Char(groups=False)
    smtp_ssl_certificate = fields.Binary(groups=False)
    smtp_ssl_private_key = fields.Binary(groups=False)

    def open_google_gmail_uri(self):
        if self.the_user_is_accessing_its_own_mail_settings():
            self = self.sudo()
        return super().open_google_gmail_uri()

    def test_smtp_connection(self):
        if self.the_user_is_accessing_its_own_mail_settings():
            self = self.sudo()
        return super().test_smtp_connection()

    def the_user_is_accessing_its_own_mail_settings(self, user):
        """
        The user is accessing its own mail settings
        if the from_filter and smtp_user are both equal to the user's login.
        """
        values = set(
            self.from_filter,
            self.smtp_user,
            self.env.user.login,
        )
        return len(values) == 1
