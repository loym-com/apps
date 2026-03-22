from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    def _compute_display_name(self):
        custom_records = self.filtered(lambda rec: rec.name and rec.partner_id.name and rec.name == rec.partner_id.name)
        super_records = self - custom_records

        for record in custom_records:
            record.display_name = record.name

        if super_records:
            super(AccountAnalyticAccount, super_records)._compute_display_name()

