import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DonationThanks(models.Model):
    _name = "donation.thanks"
    _description = "Donation Thanks"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        ondelete="restrict",
    )
    partner_display_name = fields.Char(
        string="Partner Display Name",
        related="partner_id.display_name",
        store=True,
    )
    thanks_template_id = fields.Many2one(
        string="Thanks Template",
        comodel_name="donation.thanks.template",
    )
    donation_ids = fields.One2many(
        string="Donations",
        comodel_name="donation.donation",
        inverse_name="thanks_id",
    )
    print_date = fields.Date(
        string="Print Date",
    )

    @api.depends("partner_id", "print_date")
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.partner_id.name} {record.write_date}"
            result.append((record.id, name))
        return result
