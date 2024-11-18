from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    birthday = fields.Date(related='partner_id.birthday', string='Date of Birth')
