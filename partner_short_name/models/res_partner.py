from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    short_name = fields.Char("Short name", index=True)
