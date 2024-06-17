from odoo import _, api, fields, models


class DonationDonation(models.Model):
    _inherit = "donation.donation"

    partner_address_ok = fields.Boolean(
        related="partner_id.address_ok",
        string="Donor address OK",
    )
    partner_email = fields.Char(
        related="partner_id.email",
        string="Donor email",
    )
    partner_lang = fields.Selection(
        related="partner_id.lang",
        string="Donor language",
    )
    partner_tag_ids = fields.Many2many(
        string="Donor Tags",
        related="partner_id.category_id",
        help="Use tags on the donor to segment e.g. communication (email / snailmail)",
    )
