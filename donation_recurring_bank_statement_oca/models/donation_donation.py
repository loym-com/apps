from odoo import Command, fields, models


class DonationDonation(models.Model):
    _inherit = "donation.donation"

    def _compute_display_name(self):
        for donation in self:
            if donation.recurring_template:
                donation.display_name = (
                    f"{donation.amount_total_company_currency}"
                    f" - from {donation.partner_id.display_name}"
                    f" since {donation.donation_date}"
                )
            else:
                super(DonationDonation, donation)._compute_display_name()
