from odoo import api, fields, models

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "code.list.mixin"]
