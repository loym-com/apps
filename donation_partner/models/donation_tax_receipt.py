from odoo import _, api, fields, models


class DonationTaxReceipt(models.Model):
    _inherit = "donation.tax.receipt"

    partner_valid_postal_address = fields.Boolean(
        related="partner_id.is_valid_postal_address",
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
        related="partner_id.category_id",
        string="Donor tags",
        help="Use tags on the donor to segment e.g. communication (email / snailmail)",
    )
