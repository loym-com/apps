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

    analytic_account_id = fields.Many2one("account.analytic.account")
    description = fields.Char(
        string="Description",
        default=lambda self: self._default_description(),
    )
    donation_date = fields.Date(
        string="Donation Date",
        related="donation_id.donation_date",
        store=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        related="donation_id.partner_id",
        store=True,
        readonly=True,
    )
    payment_ref = fields.Char(
        string="Payment Reference",
        related="donation_id.payment_ref",
        store=True,
        readonly=True,
    )
