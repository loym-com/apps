from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    mail_server_id = fields.Many2one(
        comodel_name="ir.mail_server",
        string="Outgoing Mail Server",
        help="The outgoing mail server used by this user to send emails.",
        compute="_compute_mail_server_id",
    )

    def _compute_mail_server_id(self):
        for user in self:
            mail_server = self.env["ir.mail_server"].search(
                [("from_filter", "=", user.login)], limit=1
            )
            user.mail_server_id = mail_server.id if mail_server else False

    def action_mail_config_by_user(self):
        """
        Create an outgoing mail server for the user if it does not exist,
        and open the form view of the mail server.
        """
        self.ensure_one()
        email = self.login
        mail_out_server = self.env["ir.mail_server"].search(
            [("from_filter", "=", email)]
        )
        if not mail_out_server:
            Config = self.env["ir.config_parameter"].sudo()
            module = "mail_config_by_user"
            # name may have {name} and/or {login} placeholders
            name = Config.get_param(f"{module}.name", default=email)
            data = {}
            if "{name}" in name:
                data['name'] = self.name
            if "{login}" in name:
                data['login'] = self.login
            name = name.format_map(data)

            smtp_authentication = Config.get_param(f"{module}.smtp_authentication")
            smtp_encryption = Config.get_param(f"{module}.smtp_encryption")
            smtp_host = Config.get_param(
                f"{module}.smtp_host", default="smtp.example.com"
            )
            smtp_port = Config.get_param(f"{module}.smtp_port")
            sequence = Config.get_param(f"{module}.sequence", default=10)
            values = {
                "name": f"{name}",
                "from_filter": email,
                "smtp_host": smtp_host,
                "sequence": sequence,
                "smtp_user": email,
            }
            if smtp_authentication:
                values["smtp_authentication"] = smtp_authentication
            if smtp_encryption:
                values["smtp_encryption"] = smtp_encryption
            if smtp_port:
                values["smtp_port"] = smtp_port
            mail_out_server = self.env["ir.mail_server"].create(values)
        mail_out_server.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'ir.mail_server',
            'res_id': mail_out_server.id,
        }
