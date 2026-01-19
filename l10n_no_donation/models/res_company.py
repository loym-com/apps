from odoo import _, api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    l10n_no_donation_partner_id = fields.Many2one(
        "res.partner", "Donation Contact Person"
    )
