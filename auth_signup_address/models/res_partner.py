from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthday = fields.Date(string='Date of Birth')
