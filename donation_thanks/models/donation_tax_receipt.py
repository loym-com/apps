from odoo import _, api, fields, models


class DonationTaxReceipt(models.Model):
    _inherit = "donation.tax.receipt"

    thanks_template_id = fields.Many2one(
        "donation.thanks.template",
        string="Thanks Template",
        ondelete="restrict",
        copy=False,
    )
