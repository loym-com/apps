from odoo import _, api, fields, models


class DonationDonation(models.Model):
    _inherit = "donation.donation"

    # def _compute_display_name(self):
    #     for donation in self:
    #         if donation.recurring_template:
    #             donation.display_name = (
    #                 f"{donation.amount_total_company_currency}"
    #                 f" - from {donation.partner_id.display_name}"
    #                 f" since {donation.donation_date}"
    #             )
    #         else:
    #             super(DonationDonation, donation)._compute_display_name()

    source_recurring_id = fields.Many2one(
        states={"done": [("readonly", False)]},
    )

    @api.depends("state", "partner_id", "move_id", "recurring_template")
    def name_get(self):
        res = []
        for donation in self:
            name = (
                f"{donation.amount_total_company_currency}"
                f" - from {donation.partner_id.display_name}"
                f" since {donation.donation_date}"
            )
            if donation.recurring_template == "active":
                pass
            elif donation.recurring_template == "suspended":
                name = _("Suspended") + " - " + name
            else:
                name = super(DonationDonation, donation).name_get()[0][1]
            res.append((donation.id, name))
        return res
