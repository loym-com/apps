import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DonationLine(models.Model):
    _inherit = "donation.line"

    @api.onchange("analytic_account_id")
    def _default_description(self):
        if self.analytic_account_id:
            self.description = self.analytic_account_id.with_context(
                lang=self.donation_id.partner_id.lang
            ).donation_description
        else:
            self.description = ""

    description = fields.Char(
        string="Description",
        default=lambda self: self._default_description(),
    )
