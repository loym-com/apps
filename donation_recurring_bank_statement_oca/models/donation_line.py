from odoo import _, api, fields, models


class DonationLine(models.Model):
    _inherit = "donation.line"

    source_recurring_id = fields.Many2one(
        "donation.donation",
        string="Recurring Template",
        related="donation_id.source_recurring_id",
        readonly=False,
    )
