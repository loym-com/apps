# Copyright 2026 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.model_create_multi
    def create(self, vals_list):
        self = self.with_context(mail_activity_quick_update=True)
        return super(MailActivity, self).create(vals_list)

    def write(self, values):
        self = self.with_context(mail_activity_quick_update=True)
        return super(MailActivity, self).write(values)
