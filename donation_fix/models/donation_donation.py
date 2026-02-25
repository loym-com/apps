from odoo import _, api, fields, models


class DonationDonation(models.Model):
    _inherit = "donation.donation"

    commercial_partner_id = fields.Many2one(
        related="partner_id",
        store=False,
    )
